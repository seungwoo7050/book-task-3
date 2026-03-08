# Contract Harness

이 프로젝트의 RN 앱은 네트워크 완성도를 목표로 하지 않는다.
대신 shared contract를 UI surface에 투영해서 아래 질문에 답한다.

- 어떤 역할이 어떤 액션을 볼 수 있는가
- incident status transition이 어떻게 해석되는가
- approval decision이 incident 상태에 어떤 영향을 주는가
- `lastEventId` replay 규칙을 화면에서 어떻게 설명할 것인가

이 접근은 server와 DTO를 바꾸지 않고도 client-side 해석을 빠르게 검증하게 해 준다.
