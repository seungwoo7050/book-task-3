# Gestures And Reanimated

Status: verified

## 한 줄 답

swipe card, reorder list, shared transition을 한 앱에 묶어 Gesture Handler와 Reanimated 상호작용을 UI thread 중심으로 학습한 프로젝트다.

## 무슨 문제를 풀었나

모바일 UI는 "동작한다"보다 "손에 붙는가"가 더 중요하다.
이 프로젝트의 질문은 "제스처, spring animation, shared transition을 JS thread 의존 없이 설계하고 설명할 수 있는가"다.

## 내가 만든 답

- swipe card의 threshold, rotation, indicator fade, spring snap을 구현했다.
- long press reorder와 drop animation, haptic feedback 흐름을 묶었다.
- shared transition과 gesture-driven dismiss를 같은 앱 안에서 재현했다.
- interaction 중심 문서를 별도 `docs/`로 정리했다.

## 무엇이 동작하나

- Tinder-style swipe card
- drag-to-reorder list
- shared transition list/detail flow
- interruptible animation과 spring 기반 복귀 동작

## 검증 명령

```bash
make -C study/foundations/03-gestures-and-reanimated/problem test
make -C study/foundations/03-gestures-and-reanimated/problem app-build
make -C study/foundations/03-gestures-and-reanimated/problem app-test
```

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [react-native/README.md](react-native/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 학습 포인트

- 제스처와 animation state를 선언적으로 나누기
- spring/threshold 판단을 재사용 가능한 규칙으로 보기
- interaction 품질을 README에서 설명 가능한 수준으로 정리하기

## 현재 상태

- 문제 정의: `verified`
- RN 구현: `verified`
- 개념 문서: `verified`
