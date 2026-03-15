# 01-incident-ops-mobile-react-native 문제지

## 왜 중요한가

최종 앱을 만들기 전에 시스템 경계와 계약 자체를 먼저 증명해야 한다. 이 프로젝트는 "모바일 클라이언트가 제품 UX 없이도 contract correctness를 보여줄 수 있는가"를 확인한다.

## 목표

incident-ops backend와 shared DTO contract를 canonical source로 유지하고, React Native harness가 그 계약을 올바르게 해석한다는 사실을 증명하는 capstone 과제다.

## 시작 위치

- `../study/capstone/01-incident-ops-mobile/problem/code/contracts/contracts.ts`
- `../study/capstone/01-incident-ops-mobile/react-native/src/contracts.ts`
- `../study/capstone/01-incident-ops-mobile/react-native/src/harnessModel.ts`
- `../study/capstone/01-incident-ops-mobile/react-native/src/IncidentOpsHarnessApp.tsx`
- `../study/capstone/01-incident-ops-mobile/react-native/tests/incident-ops-harness.test.tsx`
- `../study/capstone/01-incident-ops-mobile/problem/script/verify_task.sh`
- `../study/capstone/01-incident-ops-mobile/react-native/app.json`
- `../study/capstone/01-incident-ops-mobile/react-native/ios/IncidentOpsMobileClient/Images.xcassets/AppIcon.appiconset/Contents.json`

## starter code / 입력 계약

- ../study/capstone/01-incident-ops-mobile/problem/code/contracts/contracts.ts에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- problem/code/contracts/contracts.ts shared DTO
- node-server/ backend reference
- react-native/ harness
- login actor selection

## 제외 범위

- `../study/capstone/01-incident-ops-mobile/problem/code/contracts/contracts.ts` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/capstone/01-incident-ops-mobile/problem/script/verify_task.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- `../study/capstone/01-incident-ops-mobile/problem/code/contracts/contracts.ts`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `initialIncident`와 `initialApproval`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `incident ops harness model`와 `acknowledges an open incident for an operator`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/capstone/01-incident-ops-mobile/problem/script/verify_task.sh` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make test && make app-build && make app-test && make server-test && make demo-e2e
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/01-incident-ops-mobile/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/01-incident-ops-mobile/react-native && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.
- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`01-incident-ops-mobile-react-native_answer.md`](01-incident-ops-mobile-react-native_answer.md)에서 확인한다.
