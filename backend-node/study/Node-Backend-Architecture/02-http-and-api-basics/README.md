# 02-http-and-api-basics

- 상태: `verified`
- 구현 레인: `node/`
- 신규 설계 여부: 신규 프로젝트

## 목표

프레임워크에 들어가기 전에 HTTP 요청/응답 모델과 REST의 기본 개념을 직접 다룬다.

## 범위

- status code
- request/response body
- JSON 직렬화
- curl/Postman 검증
- in-memory HTTP 서버

## 현재 상태

문제 설명, 프레임워크 없는 HTTP 서버 구현, 테스트를 추가했고 새 경로에서 다시 검증했다.

## 실행 명령

- 구현 경로: `node/`
- install: `pnpm install`
- build: `pnpm run build`
- test: `pnpm run test`
- run server: `pnpm start`

## 검증 상태

- `node/`: `pnpm run build && pnpm run test`

## 실패 시 복구 루트

- `415`나 `400` 응답이 나오면 `Content-Type: application/json` 헤더와 요청 본문 형식을 먼저 확인한다.
- 라우팅 테스트가 실패하면 `GET /books/:id` 경로 파싱과 JSON body 읽기 헬퍼부터 본다.
