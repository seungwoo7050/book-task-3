# 05-auth-and-authorization structure plan

이 문서는 JWT 기능 소개보다 `401`과 `403`를 어디서 갈라 놓았는지가 먼저 읽혀야 한다. 읽는 축은 `auth service -> request boundary -> public/protected route verification`이 좋다.

## 읽기 구조

1. register/login을 service에 먼저 둔 이유를 보여 준다.
2. Express middleware chain과 Nest guard chain이 각각 무엇을 담당하는지 비교한다.
3. public GET과 protected POST가 같은 e2e 맥락에서 왜 중요한지 설명한다.

## 반드시 남길 근거

- Express/Nest auth service
- Express `authMiddleware`
- Express `requireRole`
- Nest `RolesGuard`
- Express/Nest e2e tests
- 두 레인의 `build && test`

## 리라이트 톤

- 보안을 무겁게 설교하는 톤보다, 경계가 어디서 갈렸는지를 보여 주는 쪽으로 쓴다.
- `401`과 `403`의 의미 차이가 자연스럽게 읽히게 정리한다.
