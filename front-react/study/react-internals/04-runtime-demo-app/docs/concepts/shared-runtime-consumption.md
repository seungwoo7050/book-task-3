# Shared Runtime Consumption

이 demo app은 runtime 코드를 앱 내부에 복사하지 않는다. `@front-react/hooks-and-events`를 workspace dependency로 소비하고, 앱 레이어는 검색, pagination, metrics 같은 기능 조합만 담당한다.

## 왜 중요한가

- internals 단계에서 만든 패키지 경계가 실제 consumer app에서도 유지된다.
- capstone이 "또 하나의 mini-react 복사본"으로 퇴화하지 않는다.
- 버그와 한계를 runtime 쪽과 app 쪽으로 나눠 설명하기 쉬워진다.
