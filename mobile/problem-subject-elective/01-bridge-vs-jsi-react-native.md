# 01-bridge-vs-jsi-react-native 문제지

## 왜 중요한가

architecture 이야기를 실제 앱과 분리해 배우면 쉽게 추상론이 된다. 이 프로젝트는 "runtime boundary의 비용 차이를 어떤 측정 단위와 결과물로 남길 것인가"를 묻는다.

## 목표

RN 0.84 기준으로 runtime 자체를 토글하는 대신, Promise + serialized payload 표면과 sync direct-call 표면을 같은 workload로 비교하는 benchmark를 만든다.

## 시작 위치

- `../study/architecture/01-bridge-vs-jsi/react-native/src/benchmark.ts`
- `../study/architecture/01-bridge-vs-jsi/react-native/src/BridgeVsJsiStudyApp.tsx`
- `../study/architecture/01-bridge-vs-jsi/react-native/.eslintrc.js`
- `../study/architecture/01-bridge-vs-jsi/react-native/.prettierrc.js`
- `../study/architecture/01-bridge-vs-jsi/react-native/tests/bridge-vs-jsi.test.tsx`
- `../study/architecture/01-bridge-vs-jsi/problem/script/verify_task.sh`
- `../study/architecture/01-bridge-vs-jsi/react-native/app.json`
- `../study/architecture/01-bridge-vs-jsi/react-native/exports/benchmark-results.json`

## starter code / 입력 계약

- `../study/architecture/01-bridge-vs-jsi/react-native/src/benchmark.ts`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 기존 bridge-vs-jsi 과제 요구사항
- async interop-style surface
- sync TurboModule/JSI-style surface
- 5-run statistics

## 제외 범위

- `../study/architecture/01-bridge-vs-jsi/problem/script/verify_task.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `RUNS`와 `computeStats`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `bridge vs jsi benchmark helpers`와 `computes statistics for each run`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/architecture/01-bridge-vs-jsi/problem/script/verify_task.sh` 등 fixture/trace 기준으로 결과를 대조했다.
- `make test && make app-build && make app-test`가 통과한다.

## 검증 방법

```bash
make test && make app-build && make app-test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/architecture/01-bridge-vs-jsi/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/architecture/01-bridge-vs-jsi/react-native && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.
- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-bridge-vs-jsi-react-native_answer.md`](01-bridge-vs-jsi-react-native_answer.md)에서 확인한다.
