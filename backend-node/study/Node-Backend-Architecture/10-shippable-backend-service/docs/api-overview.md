# API Overview

## 공개 엔드포인트

- `POST /auth/register`
- `POST /auth/login`
- `GET /books`
- `GET /books/:id`
- `GET /health/live`
- `GET /health/ready`
- `GET /docs`

## 보호 엔드포인트

- `POST /books`
- `PUT /books/:id`
- `DELETE /books/:id`

보호 엔드포인트는 JWT 인증과 `ADMIN` role을 모두 요구한다.

## 응답 규약

- 성공: `{ "success": true, "data": ... }`
- 실패: `{ "success": false, "error": { "status": number, "message": string, "details"?: unknown } }`

## 왜 Swagger를 추가했는가

- recruiter가 코드보다 먼저 HTTP 인터페이스를 확인할 수 있다.
- DTO와 entity에 붙인 metadata가 API 가독성을 높인다.
- `09`에는 없던 “브라우저에서 바로 읽히는 설명서” 역할을 한다.
