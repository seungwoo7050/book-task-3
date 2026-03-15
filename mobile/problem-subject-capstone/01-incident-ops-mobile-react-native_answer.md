# 01-incident-ops-mobile-react-native 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

incident-ops backend와 shared DTO contract를 canonical source로 유지하고, React Native harness가 그 계약을 올바르게 해석한다는 사실을 증명하는 capstone 과제다. 핵심은 `initialIncident`와 `initialApproval`, `initialAuditLogs` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- problem/code/contracts/contracts.ts shared DTO
- node-server/ backend reference
- react-native/ harness
- 첫 진입점은 `../study/capstone/01-incident-ops-mobile/react-native/src/contracts.ts`이고, 여기서 `initialIncident`와 `initialApproval` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/capstone/01-incident-ops-mobile/react-native/src/contracts.ts`: 핵심 구현을 담는 파일이다.
- `../study/capstone/01-incident-ops-mobile/react-native/src/harnessModel.ts`: `initialIncident`, `initialApproval`, `initialAuditLogs`, `streamEvents`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/capstone/01-incident-ops-mobile/react-native/src/IncidentOpsHarnessApp.tsx`: `IncidentOpsHarnessApp`, `styles`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/capstone/01-incident-ops-mobile/problem/code/contracts/contracts.ts`: `USER_ROLES`, `INCIDENT_SEVERITIES`, `INCIDENT_STATUSES`, `APPROVAL_DECISIONS`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/capstone/01-incident-ops-mobile/react-native/.eslintrc.js`: 핵심 구현을 담는 파일이다.
- `../study/capstone/01-incident-ops-mobile/react-native/tests/incident-ops-harness.test.tsx`: `incident ops harness model`, `acknowledges an open incident for an operator`, `requests and approves resolution`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/capstone/01-incident-ops-mobile/problem/script/verify_task.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.
- `../study/capstone/01-incident-ops-mobile/react-native/app.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.

## 정답을 재구성하는 절차

1. `../study/capstone/01-incident-ops-mobile/problem/code/contracts/contracts.ts`와 `../study/capstone/01-incident-ops-mobile/react-native/src/contracts.ts`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `incident ops harness model` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make test && make app-build && make app-test && make server-test && make demo-e2e`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test && make app-build && make app-test && make server-test && make demo-e2e
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/01-incident-ops-mobile/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/01-incident-ops-mobile/react-native && npm run verify
```

- `../study/capstone/01-incident-ops-mobile/problem/code/contracts/contracts.ts` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `incident ops harness model`와 `acknowledges an open incident for an operator`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test && make app-build && make app-test && make server-test && make demo-e2e`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/capstone/01-incident-ops-mobile/react-native/src/contracts.ts`
- `../study/capstone/01-incident-ops-mobile/react-native/src/harnessModel.ts`
- `../study/capstone/01-incident-ops-mobile/react-native/src/IncidentOpsHarnessApp.tsx`
- `../study/capstone/01-incident-ops-mobile/problem/code/contracts/contracts.ts`
- `../study/capstone/01-incident-ops-mobile/react-native/.eslintrc.js`
- `../study/capstone/01-incident-ops-mobile/react-native/tests/incident-ops-harness.test.tsx`
- `../study/capstone/01-incident-ops-mobile/problem/script/verify_task.sh`
- `../study/capstone/01-incident-ops-mobile/react-native/app.json`
- `../study/capstone/01-incident-ops-mobile/react-native/ios/IncidentOpsMobileClient/Images.xcassets/AppIcon.appiconset/Contents.json`
- `../study/capstone/01-incident-ops-mobile/react-native/ios/IncidentOpsMobileClient/Images.xcassets/Contents.json`
