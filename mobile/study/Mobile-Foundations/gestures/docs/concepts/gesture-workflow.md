# Gesture Workflow

이 앱의 세 데모는 모두 같은 질문을 다룬다.

1. 입력이 언제 의도가 되나
2. threshold를 넘지 못하면 어디로 되돌아가나
3. threshold를 넘으면 어떤 spring 또는 timing으로 상태가 닫히나

## Shared Rules

- swipe card: 가로 이동량이 threshold를 넘으면 dismiss, 아니면 center로 spring
- reorder list: drag offset이 행 높이를 넘을 때 index swap
- shared transition: detail 화면이 열린 뒤 swipe-down이 일정 비율을 넘으면 reverse dismiss
