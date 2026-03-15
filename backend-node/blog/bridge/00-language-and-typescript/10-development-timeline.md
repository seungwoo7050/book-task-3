# 00-language-and-typescript 개발 타임라인

`00-language-and-typescript`는 TypeScript 키워드를 한 번씩 써 보는 프로젝트가 아니다. 실제로 따라가 보면 가장 먼저 세워지는 건 문법이 아니라 신뢰 경계다. 어떤 입력부터는 그대로 믿지 않고, 어떤 실패는 전체가 아니라 항목별 결과로 되돌리며, CLI는 어떤 메시지와 exit code를 약속할지부터 정한다.

## 1. 출발점은 "타입을 배운다"가 아니라 입력을 정리하는 기준을 세우는 일이었다

문제 정의는 도서 메타데이터 CLI를 만들며 타입 모델링과 비동기 흐름을 익히라고 하지만, 코드가 실제로 보여 주는 중심은 더 구체적이다. `BookDraft`는 사용자가 준 외부 입력이고, `NormalizedBook`은 내부에서 믿고 쓸 수 있는 상태다. 이 프로젝트가 bridge인 이유는 바로 여기 있다. 프레임워크가 들어오기 전에, 입력 shape를 언제 정리할지 먼저 합의한다.

`docs/concepts/type-modeling.md`도 같은 말을 한다. 외부 입력과 내부 정규화 상태를 구분하는 습관이 뒤의 DTO, controller/service 경계, repository 반환 타입 설계의 기초가 된다는 것이다.

## 2. `normalizeTags`와 `toNormalizedBook`이 첫 번째 신뢰 경계를 만든다

가장 먼저 읽어야 할 곳은 `catalog.ts`의 정규화 함수들이다.

```ts
export function normalizeTags(tags: string[]): string[] {
  return [...new Set(tags.map(toSlugPart).filter((tag) => tag.length > 0))].sort();
}
```

여기서는 단순히 문자열을 예쁘게 다듬는 것이 아니라, 이후 단계가 더 이상 공백, 대소문자, 중복 태그를 신경 쓰지 않아도 되게 만든다. `toNormalizedBook()`도 같은 역할을 이어받는다. slug는 `title + publishedYear`로 고정하고, description이 비어 있으면 summary fallback을 만든다.

이 설계 덕분에 내부 코드가 다루는 값은 "사용자가 준 원본"이 아니라 "정규화가 끝난 상태"가 된다. 타입은 그 상태를 문서처럼 붙잡아 두는 역할을 한다.

## 3. 비동기 inventory는 앱 기능이 아니라 실패 격리 연습으로 들어온다

이 프로젝트가 작지만 좋은 이유 중 하나는 비동기 흐름을 과장하지 않는다는 점이다. `fetchInventorySnapshot()`는 inventory client를 받아 slug별 재고를 가져오지만, 실패를 `throw`로 전체에 전파하지 않고 항목별 결과로 흡수한다.

```ts
return Promise.all(
  slugs.map(async (slug) => {
    try {
      const inStock = await client.fetchStock(slug);
      return { slug, inStock };
    } catch (error) {
      return {
        slug,
        inStock: null,
        error: error instanceof Error ? error.message : "Unknown inventory error",
      };
    }
  }),
);
```

여기서 중요한 건 `Promise.all` 자체가 아니라 실패를 어디에 두는지다. 깨진 항목 하나가 전체 목록을 망치지 않도록, 오류를 result shape 안으로 넣는다. 이건 뒤에서 API 응답이나 batch job 결과를 설계할 때 그대로 다시 만나게 되는 감각이다.

다만 현재 범위도 분명하다. 이 async helper는 테스트와 헬퍼 레벨에서만 쓰이고, 실제 CLI는 inventory 조회를 호출하지 않는다. 그래서 CLI 출력의 마지막 줄은 항상 `Inventory: not requested`다. 즉 비동기 설계는 소개됐지만, 아직 end-to-end 사용자 흐름에 연결된 것은 아니다.

## 4. CLI는 마지막에 붙는 껍데기가 아니라 런타임 계약이 된다

`cli.ts`는 이 프로젝트를 "타입 유틸리티 모음"에서 "실행 가능한 도구"로 바꾸는 지점이다. `parseArgs()`는 `--title`, `--author`, `--year`, `--tags`를 필수 플래그로 강제하고, `runCli()`는 stdout/stderr와 exit code를 명시적으로 돌려준다.

```ts
export function runCli(args: string[], stdout: WriteTarget, stderr: WriteTarget): number {
  try {
    const draft = parseArgs(args);
    const normalized = toNormalizedBook(draft);
    stdout.write(`${formatBookCard(normalized)}\n`);
    return 0;
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown CLI error";
    stderr.write(`${message}\n`);
    return 1;
  }
}
```

이 함수가 중요한 이유는 예외를 없애서가 아니라, 오류를 사람이 읽을 메시지와 프로세스 종료 코드로 바꿨기 때문이다. 테스트도 정확히 그 점을 본다. 잘못된 입력이면 `stderr.write("Required flags: ...")`와 `exitCode === 1`이 같이 나와야 한다.

여기서 현재 구현의 작은 어긋남도 하나 보인다. `parseArgs()`는 `publishedYear < 0`일 때만 막기 때문에 `0`은 허용하지만, 오류 메시지는 `--year must be a positive integer`라고 적는다. 즉 메시지와 실제 경계가 완전히 일치하지는 않는다. 이런 사소한 어긋남을 빨리 보는 감각도 bridge 프로젝트의 가치다.

## 5. 테스트는 문법 지식이 아니라 경계 설계를 고정한다

`ts/tests/catalog.test.ts`는 여섯 개 테스트로 이 프로젝트의 중심을 정확히 묶어 둔다.
- 태그 정규화와 중복 제거
- `BookDraft -> NormalizedBook`
- 배치 inventory 실패 격리
- human-readable card formatting
- CLI 성공
- CLI 실패

즉 테스트가 확인하는 건 TypeScript 문법 자체가 아니라, 어떤 값이 내부에서 신뢰 가능한 상태인지와 실패를 어떤 모양으로 노출할지다.

## 6. 이번 재실행은 워크스페이스는 건강하지만 예제 스크립트 경로 가정이 있음을 보여 줬다

이번 턴에서 실제로 돌린 검증은 아래와 같았다.

```bash
pnpm run build
pnpm run test
pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"
bash problem/script/run-example.sh
```

결과는 분명했다.
- `pnpm run build`: 통과
- `pnpm run test`: `6` tests passed
- `pnpm start ...`: 카드 출력 정상
- `run-example.sh`: 상위 폴더에서 돌리면 `ERR_PNPM_NO_IMPORTER_MANIFEST_FOUND`

즉 실제 TypeScript 워크스페이스는 닫혀 있지만, 문제 폴더에 있는 실행 스크립트는 현재 작업 디렉터리를 `ts/`로 옮기지 않기 때문에 재현 명령으로는 불완전하다. 문서도 이 차이를 숨기지 않는 편이 맞다.

## 정리

이 프로젝트는 아주 작지만, 이후 백엔드 프로젝트 전체에 계속 남는 세 가지 감각을 먼저 심어 준다. 입력은 바로 믿지 말고 정규화할 것, 비동기 실패는 전체가 아니라 항목별 결과로 가둘 것, CLI든 HTTP든 오류는 사람이 읽는 메시지와 명시적 종료 신호로 닫을 것. 바로 그 점 때문에 이 글은 bridge의 첫 장으로 읽을 가치가 있다.
