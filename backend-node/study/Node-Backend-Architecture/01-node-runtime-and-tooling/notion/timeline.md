# 01-node-runtime-and-tooling — 개발 타임라인

이 문서는 프로젝트의 전체 개발 과정을 순서대로 기록한다.
소스 코드만으로는 알 수 없는 설치 과정, CLI 명령, 파일 생성 순서 등을 담는다.

---

## 1단계: 프로젝트 초기화

### 디렉토리 생성

```bash
mkdir -p 01-node-runtime-and-tooling/node/src
mkdir -p 01-node-runtime-and-tooling/node/tests
mkdir -p 01-node-runtime-and-tooling/problem/code
mkdir -p 01-node-runtime-and-tooling/problem/data
mkdir -p 01-node-runtime-and-tooling/problem/script
mkdir -p 01-node-runtime-and-tooling/docs/concepts
mkdir -p 01-node-runtime-and-tooling/docs/references
```

구조는 이전 과제와 동일하다:
- `node/` — 실제 구현 코드와 테스트 (이 프로젝트부터 구현 레인 이름이 `ts/`에서 `node/`로 바뀐다)
- `problem/` — 과제 설명, 스타터 코드, 샘플 데이터
- `docs/` — 개념 문서와 참조 자료

### 패키지 초기화

```bash
cd node
pnpm init
```

### 의존성 설치

```bash
pnpm add -D typescript @types/node vitest
```

이전 과제와 동일한 devDependencies 구성이다. 런타임 의존성은 없다.

### TypeScript, Vitest 설정

- `tsconfig.json`: 루트의 `tsconfig.base.json`을 extends, `outDir: ./dist`, `rootDir: ./src`
- `vitest.config.ts`: `environment: "node"`, `globals: true`

### npm 스크립트

```json
{
  "build": "tsc",
  "start": "node dist/cli.js",
  "test": "vitest run"
}
```

---

## 2단계: 샘플 데이터 준비 (problem/data/)

### NDJSON 로그 파일 작성

`problem/data/request-log.ndjson` — 5개의 요청 레코드를 NDJSON 형식으로 작성했다:
- 3명의 사용자 (`u1`, `u2`, `u3`)
- 3개의 경로 (`/books`, `/books/1`, `/health`)
- 2개의 에러 응답 (404, 500)

이 파일은 구현 코드의 입력이자 테스트의 fixture로 사용된다.

---

## 3단계: 문제 정의 (problem/)

### 스타터 코드 작성

`problem/code/starter.ts` — `RequestRecord`, `RequestSummary` 타입과 함수 시그니처를 제공했다.

### 과제 지침서 작성

`problem/README.md` — NDJSON을 스트림으로 읽고, 환경 변수로 출력 형식을 바꾸고, 에러 시 실패 지점을 드러내라는 요구사항을 명시했다.

### 예시 실행 스크립트

`problem/script/run-example.sh`:
```bash
REPORT_FORMAT=json pnpm start -- ../problem/data/request-log.ndjson
```

---

## 4단계: 핵심 모듈 구현 (node/src/request-report.ts)

### 구현 순서

1. **타입 정의**: `RequestRecord` (timestamp, userId, route, status)와 `RequestSummary` (filePath, totalRequests, uniqueUsers, errorCount, perRoute)를 확정했다.

2. **`readRequestLog` 구현**: 
   - `path.resolve`로 경로 정규화
   - `fs.stat`으로 파일 존재 확인 (존재하지 않으면 자동으로 에러)
   - `createReadStream` + `readline.createInterface`로 줄 단위 스트리밍 읽기
   - 빈 줄 건너뛰기
   - 파싱 실패 시 줄 번호 포함한 에러 메시지 생성

3. **`summarizeRequests` 구현**: 
   - `Set`으로 고유 사용자 카운팅
   - `Record<string, number>`로 경로별 호출 수 집계
   - `status >= 400`으로 에러 카운팅
   - 단일 순회로 모든 통계를 한 번에 계산

4. **`formatSummary` 구현**: 
   - `json` 형식: `JSON.stringify(summary, null, 2)`
   - `text` 형식: 사람이 읽기 좋게 경로별 통계를 알파벳 순으로 정렬해서 출력

---

## 5단계: CLI 구현 (node/src/cli.ts)

### 구현 내용

- `args[0]`에서 파일 경로를 받는다 (없으면 usage 메시지와 함께 종료 코드 1)
- `env.REPORT_FORMAT`에서 출력 형식을 받는다 (기본값: `"text"`, 허용값: `"text"` | `"json"`)
- 잘못된 형식이면 에러 메시지와 함께 종료 코드 1
- `readRequestLog` → `summarizeRequests` → `formatSummary` 파이프라인으로 처리
- `stdout`, `stderr`, `env`를 모두 주입 가능하게 해서 테스트에서 교체 가능

### require.main 가드

`require.main === module` 패턴으로 직접 실행과 import를 구분했다. 비동기 함수이므로 `.then()`으로 종료 코드를 설정한다.

---

## 6단계: 테스트 작성 (node/tests/request-report.test.ts)

### 테스트 항목

1. **파일 읽기**: fixture 파일에서 5개 레코드가 정상적으로 파싱되는지 확인
2. **요약 계산**: totalRequests=5, uniqueUsers=3, errorCount=2, `/books` 호출 수=3인지 확인
3. **텍스트 포맷**: `"Total requests: 5"`와 `"- /books: 3"` 같은 텍스트가 출력에 포함되는지 확인
4. **CLI JSON 모드**: `REPORT_FORMAT=json`으로 실행하면 JSON 출력에 `"totalRequests": 5`가 포함되는지 확인
5. **CLI 에러 처리**: 잘못된 형식(`yaml`)을 넣으면 에러 메시지와 종료 코드 1을 반환하는지 확인

### fixture 경로 해석

테스트에서 fixture 파일 경로를 `path.resolve(__dirname, "../../problem/data/request-log.ndjson")`으로 해석한다. 이건 테스트 파일 위치(`node/tests/`)에서 상대 경로로 `problem/data/`를 찾는 것이다.

---

## 7단계: 빌드와 검증

### 빌드

```bash
cd node
pnpm run build
```

### 테스트 실행

```bash
pnpm run test
```

5개 테스트 케이스 전체 통과.

### CLI 수동 실행 — 텍스트 형식

```bash
pnpm start -- ../problem/data/request-log.ndjson
```

출력 예시:
```
File: /absolute/path/to/request-log.ndjson
Total requests: 5
Unique users: 3
Error count: 2
Per route:
- /books: 3
- /books/1: 1
- /health: 1
```

### CLI 수동 실행 — JSON 형식

```bash
REPORT_FORMAT=json pnpm start -- ../problem/data/request-log.ndjson
```

출력 예시:
```json
{
  "filePath": "/absolute/path/to/request-log.ndjson",
  "totalRequests": 5,
  "uniqueUsers": 3,
  "errorCount": 2,
  "perRoute": {
    "/books": 3,
    "/books/1": 1,
    "/health": 1
  }
}
```

---

## 8단계: 문서 작성 (docs/)

### 개념 문서

`docs/concepts/streaming-cli.md` — 스트리밍 CLI를 만들 때의 체크리스트를 정리했다. 입력 경로 해석, NDJSON 형식 확정, 메모리 효율, 환경 변수 기본값 문서화 등.

### 참조 자료

`docs/references/checked-sources.md` — Node.js 공식 문서의 `fs`와 `readline` API를 다시 확인하고, 학습한 내용을 기록했다.

### 프로젝트 README

루트 `README.md` — 상태, 목표, 범위, 실행 명령, 검증 상태, 실패 시 복구 루트를 기록했다.

---

## 프로젝트 파일 구조 최종 상태

```
01-node-runtime-and-tooling/
├── README.md
├── docs/
│   ├── README.md
│   ├── concepts/
│   │   └── streaming-cli.md
│   └── references/
│       └── checked-sources.md
├── problem/
│   ├── README.md
│   ├── code/
│   │   └── starter.ts
│   ├── data/
│   │   └── request-log.ndjson
│   └── script/
│       └── run-example.sh
└── node/
    ├── package.json
    ├── pnpm-lock.yaml
    ├── tsconfig.json
    ├── vitest.config.ts
    ├── src/
    │   ├── request-report.ts
    │   └── cli.ts
    └── tests/
        └── request-report.test.ts
```

---

## 사용한 도구 요약

| 도구 | 용도 |
|------|------|
| pnpm | 패키지 매니저 |
| TypeScript 5.6+ | 컴파일러 |
| Vitest 2.1+ | 테스트 러너 |
| Node.js fs, path, readline | 파일 시스템, 경로 처리, 줄 단위 스트리밍 |
| process.env | 환경 변수를 통한 출력 형식 제어 (`REPORT_FORMAT`) |
