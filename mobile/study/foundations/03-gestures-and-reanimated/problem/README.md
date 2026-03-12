# Problem: Gestures And Reanimated

> Status: VERIFIED
> Scope: interaction-heavy RN UI
> Last Checked: 2026-03-12

## 문제 요약

Swipe card, reorder list, shared transition 세 기능을 구현해 Gesture Handler와 Reanimated 기반 상호작용을 검증한다.
핵심은 애니메이션이 UI thread 중심으로 동작하고, gesture 종료 조건과 spring 동작을 설명 가능하게 만드는 것이다.

## 왜 이 문제가 커리큘럼에 필요한가

navigation과 list 성능이 "구조"를 다뤘다면, 이 프로젝트는 "체감 품질"을 다룬다.
이 단계가 있어야 이후 제품형 앱에서 사용자의 손맛과 복귀 애니메이션을 설계 관점으로 설명할 수 있다.

## 제공 자료

- 기존 gestures 과제 요구사항
- `problem/code/README.md`의 구현 스캐폴드
- `problem/data/README.md`의 참고 자료

## 필수 요구사항

1. threshold와 spring snap이 있는 swipe card
2. long press 기반 reorder list
3. haptic feedback과 visual feedback
4. shared transition list/detail flow
5. gesture-driven dismiss와 interruptible animation

## 의도적 비범위

- 커스텀 native gesture recognizer 작성
- production asset pipeline
- physics engine 수준의 세밀한 튜닝

## 평가/검증 기준

```bash
make test
```

- swipe threshold와 spring 복귀가 일관돼야 한다.
- reorder 시 position swap과 drop animation이 정상 동작해야 한다.
- shared transition이 dismiss gesture로 역재생돼야 한다.
- 앱 빌드와 테스트가 재현 가능해야 한다.

## 원문/출처 보존 위치

- [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
