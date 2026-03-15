# 02-http-and-api-basics Structure Plan

## 한 줄 초점
- frameworkless HTTP 서버를 통해, 프레임워크가 평소 가려 주던 반복 작업과 실패 status code 분기를 드러낸다.

## 독자 질문
- request body parsing, route matching, response serialization은 실제로 어디서 일어나는가?
- `BookStore`와 validator를 분리하면 왜 route handler가 읽기 쉬워지는가?
- `400/404/415`를 나누는 기준과 현재 테스트 커버리지는 어떻게 다른가?

## 본문 구성
1. 문제 재정의
   CRUD보다 프레임워크 없는 HTTP 반복 작업이 중심이라는 점을 잡는다.
2. HTTP skeleton
   `readJsonBody`, `sendJson`, `matchBookId`를 본다.
3. 도메인 경계
   `BookStore`, validator, in-memory state를 본다.
4. 실패 계약
   malformed JSON, invalid payload, wrong content-type, missing book/route를 나눈다.
5. 실제 재현
   build/test와 순차 HTTP 호출 결과를 닫는다.

## 반드시 연결할 증거
- `node/src/app.ts`
  route/body/status code 분기
- `node/src/book-store.ts`
  store와 validator
- `node/tests/app.test.ts`
  현재 test-covered branch
- `problem/script/curl-examples.sh`
  최소 curl 재현 기준

## 서술 원칙
- 기존 blog 문장을 입력으로 삼지 않는다.
- 성공 CRUD보다 HTTP 실패 경로의 의미를 더 선명하게 쓴다.
- 테스트가 덮는 영역과 소스만으로 확인된 영역을 구분한다.

## 이번 턴의 결론 문장
- `02-http-and-api-basics`는 작은 CRUD 서버를 통해, 이후 Express와 NestJS가 자동으로 흡수할 HTTP 반복 작업을 한 번 직접 드러내는 bridge 프로젝트다.
