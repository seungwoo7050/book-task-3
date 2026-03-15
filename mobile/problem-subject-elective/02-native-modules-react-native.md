# 02-native-modules-react-native 문제지

## 왜 중요한가

RN architecture를 이해한 뒤에는 경계를 실제 모듈 계약으로 내려와야 한다. 이 프로젝트는 "네이티브 연동을 기능 구현이 아니라 public contract 설계 문제로 다룰 수 있는가"를 확인한다.

## 목표

Battery, Haptics, Sensor 세 모듈의 TypeScript public spec을 고정하고, codegen summary와 consumer app을 통해 JS/native 경계를 설명하는 과제다.

## 시작 위치

- `../study/architecture/02-native-modules/react-native/src/NativeModulesStudyApp.tsx`
- `../study/architecture/02-native-modules/react-native/src/specs.ts`
- `../study/architecture/02-native-modules/react-native/.eslintrc.js`
- `../study/architecture/02-native-modules/react-native/.prettierrc.js`
- `../study/architecture/02-native-modules/react-native/tests/native-modules.test.tsx`
- `../study/architecture/02-native-modules/problem/script/verify_task.sh`
- `../study/architecture/02-native-modules/react-native/app.json`
- `../study/architecture/02-native-modules/react-native/generated/modules.json`

## starter code / 입력 계약

- `../study/architecture/02-native-modules/react-native/src/NativeModulesStudyApp.tsx`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 기존 native-modules 과제 요구사항
- typed module specs
- codegen summary export
- consumer screen

## 제외 범위

- `../study/architecture/02-native-modules/problem/script/verify_task.sh` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `NativeModulesStudyApp`와 `styles`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `native modules specs`와 `defines three module specs`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/architecture/02-native-modules/problem/script/verify_task.sh` 등 fixture/trace 기준으로 결과를 대조했다.
- `make test && make codegen && make app-build && make app-test`가 통과한다.

## 검증 방법

```bash
make test && make codegen && make app-build && make app-test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/architecture/02-native-modules/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/architecture/02-native-modules/react-native && npm run verify
```

- Node 계열 lab는 의존성 설치(`npm install` 등)가 끝난 뒤 검증 명령을 실행한다.
- Spring/Java 계열 검증은 `JDK/JRE`가 현재 머신에 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`02-native-modules-react-native_answer.md`](02-native-modules-react-native_answer.md)에서 확인한다.
