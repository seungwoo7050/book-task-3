# Navigation Patterns

Status: verified

## 한 줄 답

Stack, Tab, Drawer, Deep Linking을 하나의 React Native 앱으로 연결하고, typed params와 fallback route까지 검증한 navigation 파일럿이다.

## 무슨 문제를 풀었나

React Native 앱에서 화면 수가 늘어나면 navigation 구조가 가장 먼저 복잡해진다.
이 프로젝트의 질문은 "중첩 navigator, custom UI, deep link state를 함께 가져가도 경로와 params를 설명 가능하게 유지할 수 있는가"다.

## 내가 만든 답

- Stack, Tab, Drawer를 한 앱 안에 중첩 구성했다.
- typed route params와 custom header/tab bar/drawer content를 같이 설계했다.
- `myapp://` 기반 deep link와 fallback screen을 연결했다.
- TypeScript와 Jest 검증으로 navigation state mapping을 고정했다.

## 무엇이 동작하나

- `Home -> Detail -> Settings -> ProfileDetail` stack 흐름
- badge와 스타일이 있는 bottom tab
- mock auth 상태에 따라 바뀌는 custom drawer action
- `home`, `detail/:id`, `profile/:userId`, `notifications`, fallback deep link 처리

## 검증 명령

```bash
make -C study/foundations/01-navigation-patterns/problem test
npm --prefix study/foundations/01-navigation-patterns/react-native run verify
```

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [react-native/README.md](react-native/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 학습 포인트

- navigation state를 화면 계층이 아니라 데이터 구조로 설명하기
- deep link path와 nested navigator state를 맞추기
- RN 앱 초기 단계에서 typed params를 습관으로 고정하기

## 현재 상태

- 문제 정의: `verified`
- RN 구현: `verified`
- 개념 문서: `verified`
