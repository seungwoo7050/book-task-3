# 00-language-and-typescript — 개발 타임라인

이 문서는 프로젝트의 전체 개발 과정을 순서대로 기록한다.
소스 코드를 직접 읽으면 "무엇이 만들어졌는지"는 알 수 있지만, "어떤 순서로, 어떤 도구를 써서 만들었는지"는 알 수 없다.
이 타임라인은 그 빈 부분을 채운다.

---

## 1단계: 프로젝트 초기화

### 디렉토리 생성

```
mkdir -p 00-language-and-typescript/ts/src
mkdir -p 00-language-and-typescript/ts/tests
mkdir -p 00-language-and-typescript/problem/code
mkdir -p 00-language-and-typescript/problem/script
mkdir -p 00-language-and-typescript/docs/concepts
mkdir -p 00-language-and-typescript/docs/references
```

프로젝트 구조는 세 갈래로 나뉜다:
- `ts/` — 실제 구현 코드와 테스트
- `problem/` — 과제 설명, 스타터 코드, 예시 실행 스크립트
- `docs/` — 개념 문서와 참조 자료

### 패키지 초기화

```bash
cd ts
pnpm init
```

`package.json`에 `name`, `version`, `private: true`를 설정했다.

### 의존성 설치

```bash
pnpm add -D typescript @types/node vitest
```

- `typescript` (^5.6.0): 컴파일러
- `@types/node` (^22.0.0): Node.js 타입 정의
- `vitest` (^2.1.0): 테스트 러너

이 프로젝트는 런타임 의존성이 없다. 모든 패키지가 `devDependencies`에 들어간다.

### TypeScript 설정

`ts/tsconfig.json`을 생성했다:
- 루트의 `tsconfig.base.json`을 `extends`한다 (경로: `../../../../tsconfig.base.json`)
- `outDir`을 `./dist`로, `rootDir`을 `./src`로 설정
- `tsconfig.base.json`에서 `strict: true`, `target: ES2022`, `module: commonjs` 등이 상속된다

### Vitest 설정

`ts/vitest.config.ts`를 생성했다:
- `environment: "node"` — Node.js 환경에서 테스트 실행
- `globals: true` — `describe`, `it`, `expect`를 import 없이 사용

### npm 스크립트 등록

`package.json`의 `scripts`:
```json
{
  "build": "tsc",
  "start": "node dist/cli.js",
  "test": "vitest run"
}
```

---

## 2단계: 문제 정의 (problem/)

### 스타터 코드 작성

`problem/code/starter.ts` — 학습자가 참고할 타입 정의와 함수 시그니처를 제공했다:
- `BookDraft`, `NormalizedBook`, `InventoryClient`, `InventorySnapshot` 타입 골격
- `normalizeTags`, `toNormalizedBook`, `fetchInventorySnapshot`, `formatBookCard` 함수 시그니처 (본문은 `throw new Error("TODO")`)

### 과제 지침서 작성

`problem/README.md` — 구현해야 할 4가지 기능과 최소 성공 기준을 명시했다.

### 예시 실행 스크립트 작성

`problem/script/run-example.sh`:
```bash
pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture, node" --description "Patterns for backend developers"
```

---

## 3단계: 핵심 모듈 구현 (ts/src/catalog.ts)

### 구현 순서

1. **타입 정의**: `BookDraft`, `NormalizedBook`, `InventoryClient`, `InventorySnapshot` 타입을 먼저 확정했다.

2. **`normalizeTags` 구현**: 문자열 배열을 받아서 소문자 slug로 변환하고, `Set`으로 중복을 제거한 뒤 정렬해서 반환한다. 내부에 `toSlugPart` 헬퍼를 두어 공백 → 하이픈, 특수문자 제거, 앞뒤 하이픈 정리를 처리했다.

3. **`toNormalizedBook` 구현**: `BookDraft`를 받아 title/author를 trim하고, slug을 생성하고, description이 없으면 자동 summary를 만들어 `NormalizedBook`을 반환한다.

4. **`fetchInventorySnapshot` 구현**: `Promise.all` 안에서 각 slug에 대해 개별 `try/catch`를 적용했다. 실패한 항목은 `inStock: null`과 에러 메시지를 담아서 반환한다.

5. **`formatBookCard` 구현**: `NormalizedBook`과 선택적 `InventorySnapshot`을 받아 사람이 읽기 좋은 여러 줄 문자열로 포맷팅한다.

---

## 4단계: CLI 구현 (ts/src/cli.ts)

### 구현 내용

- `readFlag` 헬퍼: `process.argv` 배열에서 `--name value` 패턴을 찾아 value를 반환한다.
- `parseArgs`: `--title`, `--author`, `--year`, `--tags`를 필수로 검증하고, `--description`은 선택적으로 처리한다. `--year`는 정수 변환 후 유효성 검사를 한다.
- `runCli`: 파싱 → 정규화 → 카드 포맷 → stdout 출력을 하나의 흐름으로 연결한다. 에러가 나면 stderr에 메시지를 쓰고 종료 코드 1을 반환한다.
- `require.main === module` 가드: 직접 실행할 때만 CLI가 동작하고, import할 때는 아무 side effect가 없다.

---

## 5단계: 테스트 작성 (ts/tests/catalog.test.ts)

### 테스트 항목

1. **`normalizeTags`**: 공백 있는 태그, 대소문자 혼용, 중복 태그를 넣어서 정규화와 중복 제거가 되는지 확인
2. **`toNormalizedBook`**: 완전한 `BookDraft`를 넣어서 slug 생성, trim, tags 정규화, 자동 summary 생성이 모두 동작하는지 확인
3. **`fetchInventorySnapshot`**: `vi.fn()`으로 모킹한 `fetchStock`에서 일부 slug만 에러를 던지게 해서, 부분 실패가 전체 실패로 번지지 않는지 확인
4. **`formatBookCard`**: inventory snapshot이 있을 때 재고 수량이 출력되는지 확인
5. **CLI 정상 경로**: 유효한 인자로 `runCli`를 호출하면 종료 코드 0과 stdout 출력이 나오는지 확인
6. **CLI 실패 경로**: 필수 인자가 빠진 상태로 호출하면 종료 코드 1과 stderr 에러 메시지가 나오는지 확인

---

## 6단계: 빌드와 검증

### 빌드

```bash
cd ts
pnpm run build
```

`tsc`가 `src/` 아래의 `.ts` 파일을 컴파일해서 `dist/`에 `.js`, `.d.ts`, `.js.map` 파일을 생성한다.

### 테스트 실행

```bash
pnpm run test
```

`vitest run`이 `tests/` 아래의 `.test.ts` 파일을 찾아서 실행한다. 전체 6개 테스트 케이스가 통과하는 것을 확인했다.

### CLI 수동 실행

```bash
pnpm start -- --title "Node Patterns" --author "Alice" --year 2024 --tags "Node, Architecture"
```

정상 출력:
```
Node Patterns (2024)
Author: Alice
Slug: node-patterns-2024
Tags: architecture, node
Summary: Alice wrote Node Patterns in 2024.
Inventory: not requested
```

---

## 7단계: 문서 작성 (docs/)

### 개념 문서

`docs/concepts/type-modeling.md` — `BookDraft`와 `NormalizedBook`의 분리가 왜 중요한지, 이 패턴이 뒤의 DTO/Entity 분리로 어떻게 이어지는지를 정리했다.

### 참조 자료

`docs/references/checked-sources.md` — TypeScript Handbook의 Everyday Types와 More on Functions를 다시 확인하고, 각각에서 무엇을 배웠는지 기록했다.

### 프로젝트 README

루트 `README.md` — 상태, 목표, 범위, 실행 명령, 검증 상태, 실패 시 복구 루트를 기록했다.

---

## 프로젝트 파일 구조 최종 상태

```
00-language-and-typescript/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── type-modeling.md
│   └── references/
│       └── checked-sources.md
├── problem/
│   ├── README.md
│   ├── code/
│   │   └── starter.ts
│   └── script/
│       └── run-example.sh
└── ts/
    ├── package.json
    ├── pnpm-lock.yaml
    ├── tsconfig.json
    ├── vitest.config.ts
    ├── src/
    │   ├── catalog.ts
    │   └── cli.ts
    └── tests/
        └── catalog.test.ts
```

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| pnpm | 패키지 매니저 — `pnpm init`, `pnpm add`, `pnpm run` |
| TypeScript 5.6+ | 컴파일러 — `tsc`로 빌드 |
| Vitest 2.1+ | 테스트 러너 — `vitest run`으로 실행 |
| Node.js (ES2022 target) | 런타임 — `node dist/cli.js`로 CLI 실행 |
