# 02-native-modules-react-native 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

Battery, Haptics, Sensor 세 모듈의 TypeScript public spec을 고정하고, codegen summary와 consumer app을 통해 JS/native 경계를 설명하는 과제다. 핵심은 `NativeModulesStudyApp`와 `styles`, `MODULE_SPECS` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 기존 native-modules 과제 요구사항
- typed module specs
- codegen summary export
- 첫 진입점은 `../study/architecture/02-native-modules/react-native/src/NativeModulesStudyApp.tsx`이고, 여기서 `NativeModulesStudyApp`와 `styles` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/architecture/02-native-modules/react-native/src/NativeModulesStudyApp.tsx`: `NativeModulesStudyApp`, `styles`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/architecture/02-native-modules/react-native/src/specs.ts`: `MODULE_SPECS`, `buildGeneratedSummary`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/architecture/02-native-modules/react-native/.eslintrc.js`: 핵심 구현을 담는 파일이다.
- `../study/architecture/02-native-modules/react-native/.prettierrc.js`: 핵심 구현을 담는 파일이다.
- `../study/architecture/02-native-modules/react-native/App.tsx`: 핵심 구현을 담는 파일이다.
- `../study/architecture/02-native-modules/react-native/tests/native-modules.test.tsx`: `native modules specs`, `defines three module specs`, `builds codegen summary`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/architecture/02-native-modules/problem/script/verify_task.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.
- `../study/architecture/02-native-modules/react-native/app.json`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.

## 정답을 재구성하는 절차

1. `../study/architecture/02-native-modules/react-native/src/NativeModulesStudyApp.tsx`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `native modules specs` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make test && make codegen && make app-build && make app-test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make test && make codegen && make app-build && make app-test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/architecture/02-native-modules/react-native && npm run test
```

```bash
cd /Users/woopinbell/work/book-task-3/mobile/study/architecture/02-native-modules/react-native && npm run verify
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `native modules specs`와 `defines three module specs`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make test && make codegen && make app-build && make app-test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/architecture/02-native-modules/react-native/src/NativeModulesStudyApp.tsx`
- `../study/architecture/02-native-modules/react-native/src/specs.ts`
- `../study/architecture/02-native-modules/react-native/.eslintrc.js`
- `../study/architecture/02-native-modules/react-native/.prettierrc.js`
- `../study/architecture/02-native-modules/react-native/App.tsx`
- `../study/architecture/02-native-modules/react-native/tests/native-modules.test.tsx`
- `../study/architecture/02-native-modules/problem/script/verify_task.sh`
- `../study/architecture/02-native-modules/react-native/app.json`
- `../study/architecture/02-native-modules/react-native/generated/modules.json`
- `../study/architecture/02-native-modules/react-native/ios/NavigationPatternsStudy/Images.xcassets/AppIcon.appiconset/Contents.json`
