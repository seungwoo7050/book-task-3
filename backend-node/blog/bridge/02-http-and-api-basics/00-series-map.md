# 02-http-and-api-basics

이 글은 bridge의 마지막 장면에서 HTTP를 프레임워크 없이 한 번 손으로 다뤄 보는 프로젝트를 다시 읽는다. 여기서 중요한 건 "서버가 돈다"가 아니라, Express나 NestJS가 평소 대신해 주던 route dispatch, body parsing, header 검사, status code 분기를 실제로 어디서 직접 하게 되는지 보는 일이다.

## 이 Todo가 붙잡는 질문
프레임워크 없이 최소 Books CRUD를 만들 때, 어떤 HTTP 규약을 직접 구현해야 하고 어떤 실패를 어떤 status code로 나눠야 이후 프레임워크 추상화가 더 잘 보이는가?

문제 정의도 이 방향을 뚜렷하게 잡는다. 목표는 frameworkless Node HTTP 서버로 `GET /books`, `GET /books/:id`, `POST /books` 중심 계약을 구현하며 HTTP 기본기를 익히는 것이다. 그래서 이 프로젝트의 핵심은 CRUD 자체보다 `readJsonBody`, `sendJson`, `matchBookId`, `validateCreateBookPayload`, `400/404/415` 분기다.

## 먼저 잡아둘 범위
- `node/src/app.ts`
  HTTP 서버 골격, route matching, JSON body parsing, response serialization을 가진다.
- `node/src/book-store.ts`
  in-memory `BookStore`와 payload validation을 분리해 route handler를 가볍게 만든다.
- `node/tests/app.test.ts`
  health, create/fetch, invalid payload, wrong content-type를 고정한다.
- `problem/script/curl-examples.sh`
  서버가 이미 떠 있다는 전제 아래 최소 curl 재현 흐름을 보여 준다.

이 프로젝트의 핵심은 작은 서버가 아니라 작은 계약이다. `POST /books`는 `application/json`이 아니면 `415`, JSON은 맞지만 필드가 틀리면 `400`, 없는 책은 `404`, 없는 route도 `404`로 닫힌다. 그리고 저장소가 in-memory라서 `GET /books/1`은 같은 프로세스 안에서 먼저 `POST /books`가 일어난 뒤에만 의미가 있다.

## 이번 글에서 따라갈 순서
1. 왜 이 프로젝트를 HTTP 입문보다 "프레임워크가 숨기는 반복 작업 확인"으로 읽어야 하는지 정리한다.
2. `app.ts`에서 body parsing과 JSON 응답을 어디서 직접 쓰는지 본다.
3. `BookStore`와 validator를 바깥으로 빼며 생긴 최소 계층 경계를 본다.
4. `400/404/415`를 어떻게 다르게 쓰는지와 현재 테스트 커버리지를 함께 본다.
5. 실제 빌드·테스트·HTTP 재현 결과를 기준으로 현재 상태를 닫는다.

## 가장 중요한 코드 신호
- `node/src/app.ts`
  frameworkless HTTP의 핵심 반복 작업이 모두 여기 있다.
- `node/src/book-store.ts`
  route 바깥으로 꺼낸 가장 작은 도메인/검증 경계다.
- `node/tests/app.test.ts`
  무엇이 이미 계약으로 고정됐고 무엇이 아직 source-only branch인지 알려 준다.
- `docs/concepts/frameworkless-http.md`
  프레임워크가 실제로 무엇을 추상화하는지 짧게 언어화한다.

## 이번 턴의 재검증 메모
- `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build`: 통과
- `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test`: 통과, `4`개 테스트 전부 성공
- `COREPACK_ENABLE_AUTO_PIN=0 pnpm start`: 서버 기동, `HTTP basics server listening on 3000`
- `curl http://localhost:3000/health`: `200 {"status":"ok"}`
- `curl http://localhost:3000/books`: 초기 `200 []`
- `POST /books` with JSON: `201`과 생성된 책 반환
- same process에서 다시 `GET /books`, `GET /books/1`: 둘 다 `200`
- wrong `content-type` POST: `415 {"message":"content-type must be application/json"}`

이 구현은 실제로 건강하게 동작한다. 다만 테스트는 malformed JSON과 missing book/route를 아직 직접 assert 하지는 않아서, 그 분기들은 지금 기준으로 source-confirmed behavior다.

## 다 읽고 나면 남는 것
- 왜 이 프로젝트가 "간단한 CRUD"보다 "프레임워크가 숨기는 HTTP 반복 작업을 손으로 보는 단계"인지 설명할 수 있다.
- body parsing, route matching, validator, in-memory store가 각각 어떤 책임을 가지는지 분리해서 볼 수 있다.
- 다음 `03-rest-api-foundations`에서 같은 문제를 Express와 NestJS로 풀 때 무엇이 추상화되는지 비교할 준비가 된다.
