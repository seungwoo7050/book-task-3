# Navigation Lifecycle

React Navigation에서는 화면이 항상 mount/unmount만으로 움직이지 않는다.
특히 탭 전환에서는 mount는 유지되고 focus/blur만 바뀌는 경우가 많다.

## Practical Rule

- mount/unmount는 리소스 생성과 정리에 사용한다
- focus/blur는 데이터 새로고침, analytics, 타이머 제어에 사용한다

## In This Pilot

- `SearchTab`은 local state를 유지하는 탭 예시다
- stack 내부 화면은 back navigation과 custom header를 통해 흐름을 보여 준다
