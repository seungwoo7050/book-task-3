# 02-incident-ops-mobile-client-react-native 문제지

## 왜 중요한가

system/contract harness만으로는 제품 완성도와 UX 판단을 설명할 수 없다. 이 프로젝트는 "같은 도메인을 유지하면서도 채용 제출용 수준의 앱으로 다시 구현할 수 있는가"를 최종적으로 묻는다.

## 목표

기존 incident-ops domain과 shared contract를 유지한 채, 실제 화면 흐름, 오프라인 복구, replay-safe realtime behavior를 갖춘 hiring-facing RN 클라이언트를 완성하는 과제다.

## 시작 위치

- `../study/capstone/02-incident-ops-mobile-client/problem/code/contracts/contracts.ts`
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/app/AppModel.tsx`
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/components/Ui.tsx`
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/contracts.ts`
- `../study/capstone/02-incident-ops-mobile-client/react-native/src/lib/api.ts`
- `../study/capstone/02-incident-ops-mobile-client/react-native/__tests__/app-shell.test.tsx`
- `../study/capstone/02-incident-ops-mobile-client/react-native/__tests__/outbox.test.ts`
- `../study/capstone/02-incident-ops-mobile-client/problem/script/verify_task.sh`

## starter code / 입력 계약

- ../study/capstone/02-incident-ops-mobile-client/problem/code/contracts/contracts.ts에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- capstone/01-incident-ops-mobile의 shared contract
- node-server/ local backend reference
- auth entry와 session restore
- incident feed, detail, create form

## 제외 범위

- `../study/capstone/02-incident-ops-mobile-client/problem/code/contracts/contracts.ts` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/capstone/02-incident-ops-mobile-client/problem/script/verify_task.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- `../study/capstone/02-incident-ops-mobile-client/problem/code/contracts/contracts.ts`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `AppModelContext`와 `createId`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `jsonResponse`와 `incident ops app shell`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/capstone/02-incident-ops-mobile-client/problem/script/verify_task.sh` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make test && make app-build && make app-test && make server-test && make demo-e2e
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/02-incident-ops-mobile-client/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/capstone/02-incident-ops-mobile-client/react-native && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.
- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-incident-ops-mobile-client-react-native_answer.md`](02-incident-ops-mobile-client-react-native_answer.md)에서 확인한다.
