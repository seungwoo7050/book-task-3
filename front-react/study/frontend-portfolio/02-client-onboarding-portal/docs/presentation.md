# Client Onboarding Portal 발표 문서

이 문서는 `Client Onboarding Portal`을 면접이나 포트폴리오 리뷰에서 설명할 때 쓰는 발표 구조다.

## 발표 목표

- 고객-facing flow를 어떻게 구조화했는지 설명한다.
- form validation, draft save, route guard, submit lifecycle을 제품 관점에서 이야기한다.
- 내부도구형 포트폴리오와 다른 판단 포인트를 보여 준다.

## 6-8분 데모 흐름

1. `/onboarding?step=review`에 직접 들어가 route guard를 먼저 보여 준다.
2. `/`로 돌아가 sign-in 후 onboarding route로 진입한다.
3. workspace step에서 validation 에러를 한 번 일부러 만들고, 수정 후 `Save draft`를 실행한다.
4. 새로고침 뒤 draft restore가 유지되는지 보여 준다.
5. invite step에서 첫 collaborator를 추가한다.
6. review step에서 `Simulate the next submit failure`를 켠 뒤 실패와 retry 성공을 연속으로 보여 준다.
7. 마지막으로 case study route에서 제품 판단 포인트를 짧게 정리한다.

## 발표 포인트

- 내부도구형 앱과 달리 이 프로젝트는 사용자의 불안 감소와 다음 행동 안내가 핵심이다.
- validation, draft restore, route guard, retry는 서로 다른 concern이지만 한 journey 안에서 이어진다.
- mock backend만 쓰더라도 submit lifecycle을 제품처럼 다루는 것이 중요했다.
