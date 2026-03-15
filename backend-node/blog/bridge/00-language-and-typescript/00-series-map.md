# 00-language-and-typescript

이 글은 `backend-node` 트랙의 첫 프로젝트를 "TypeScript 문법 맛보기"로 읽지 않기 위해 다시 쓴다. 실제 문제는 문법 소개보다 먼저, 지저분한 입력을 언제 믿을 수 있는 내부 표현으로 바꿀지와 비동기 실패를 어디에 가둘지를 정하는 데 있다.

## 이 Todo가 붙잡는 질문
Express나 NestJS로 가기 전에, free-form CLI 입력과 비동기 helper를 어떤 타입 경계와 오류 계약으로 먼저 고정해야 이후 레이어가 덜 흔들리는가?

문제 정의도 그 방향을 분명히 잡는다. 목표는 작은 도서 메타데이터 CLI를 만들면서 타입 모델링, 비동기 흐름, 테스트를 한 번에 익히는 것이다. 그래서 이 프로젝트의 중심은 프레임워크가 아니라 `BookDraft -> NormalizedBook`, 항목 단위 inventory 결과, CLI exit code다.

## 먼저 잡아둘 범위
- `ts/src/catalog.ts`
  입력용 `BookDraft`와 내부용 `NormalizedBook`을 분리하고, slug/tags/summary 정규화 규칙을 정의한다.
- `ts/src/catalog.ts`의 `fetchInventorySnapshot`
  비동기 재고 조회를 전부 실패시키지 않고 slug별 결과로 흡수한다.
- `ts/src/cli.ts`
  필수 플래그 검증, stderr 메시지, exit code를 명시적 계약으로 만든다.
- `ts/tests/catalog.test.ts`
  정규화, 비동기 실패 격리, CLI 성공/실패를 고정한다.

여기서 중요한 건 범위의 작음이 아니라 경계의 선명함이다. 실제 CLI는 inventory 조회를 호출하지 않고 항상 `Inventory: not requested`를 출력한다. 즉 이 프로젝트는 "비동기 도서 앱"이 아니라, 이후 프로젝트에서 재사용할 타입/오류 규약을 먼저 익히는 브리지다.

## 이번 글에서 따라갈 순서
1. 왜 `BookDraft`를 바로 출력하지 않고 `NormalizedBook`으로 한 번 더 바꾸는지 본다.
2. `normalizeTags`와 `toNormalizedBook`이 어떤 값을 내부에서 믿을 수 있는 상태로 만드는지 본다.
3. `fetchInventorySnapshot`이 배치 비동기 실패를 어떻게 항목별로 가두는지 본다.
4. `runCli`가 단순 wrapper가 아니라 stdout/stderr/exit code 계약이 되는 순간을 본다.
5. 실제 재실행 결과와 현재 스크립트 한계를 함께 닫는다.

## 가장 중요한 코드 신호
- `ts/src/catalog.ts`
  slug, tags, summary 규칙과 inventory helper가 이 프로젝트의 핵심이다.
- `ts/src/cli.ts`
  필수 플래그와 에러 메시지를 어디서 닫는지 보여 준다.
- `ts/tests/catalog.test.ts`
  언어 브리지라는 말이 추상으로 남지 않게 만들어 주는 가장 강한 증거다.
- `docs/concepts/type-modeling.md`
  외부 입력과 내부 정규화 상태를 왜 구분하는지 개념 언어를 제공한다.

## 이번 턴의 재검증 메모
- `pnpm run build`: 통과
- `pnpm run test`: 통과, `6`개 테스트 전부 성공
- `pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"`: 정상 출력
- `bash problem/script/run-example.sh`: 실패, 상위 폴더에서 실행되면 `ERR_PNPM_NO_IMPORTER_MANIFEST_FOUND`

즉, 핵심 TypeScript 워크스페이스는 실제로 잘 닫히지만, 문제 폴더의 예제 스크립트는 현재 작업 디렉터리를 `ts/`로 옮겨 주지 않아 그대로는 재현 지점이 되지 못한다. 이 차이까지 포함해서 지금의 사실이다.

## 다 읽고 나면 남는 것
- 왜 이 프로젝트가 문법 복습이 아니라 입력/출력 계약의 출발점인지 설명할 수 있다.
- 타입 모델링이 필드 선언보다 정규화 경계를 세우는 일에 가깝다는 감각을 얻게 된다.
- 다음 `01-node-runtime-and-tooling`에서 왜 파일, env, stream 같은 런타임 입력으로 넘어가야 하는지 자연스럽게 연결된다.
