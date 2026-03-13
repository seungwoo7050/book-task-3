# 02-http-and-api-basics evidence ledger

이 프로젝트도 path 단위 `git log`는 `2026-03-12` 한 번의 이관 커밋만 보여 준다. 아래 표는 `app.ts`, `book-store.ts`, 테스트, 재검증 CLI를 바탕으로 구현 순서를 다시 세운 것이다.

| 순서 | 시간 표지 | 당시 목표 | 변경 단위 | 처음 가설 | 실제 조치 | CLI | 검증 신호 | 핵심 코드 앵커 | 새로 배운 것 | 다음 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Phase 1 | 프레임워크 없이 HTTP 서버의 최소 골격을 직접 세운다 | `node/src/app.ts`의 `readJsonBody`, `sendJson`, route 분기 | health와 books 몇 개면 조건문만으로 금방 끝날 것 같았다 | body 읽기, JSON 직렬화, `Content-Type`, route matching을 모두 명시적으로 적었다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run build` | `build: ok` | `if (method === "GET" && url === "/health")` | 프레임워크가 숨겨 주는 일은 결국 body parsing, 헤더 설정, route 분기 같은 반복 작업이었다 | 도메인 규칙을 밖으로 빼야 한다 |
| 2 | Phase 2 | 메모리 저장소와 payload 검증으로 HTTP 계층을 가볍게 만든다 | `node/src/book-store.ts`의 `BookStore`, `validateCreateBookPayload` | 작은 예제니까 `app.ts` 안에서 `Map`을 직접 조작해도 충분해 보였다 | 저장소와 validator를 분리해 route handler가 도메인 규칙을 전부 들고 있지 않게 했다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test` | `Test Files 1 passed`, `Tests 4 passed` | `if (typeof publishedYear !== "number" || !Number.isInteger(publishedYear))` | 작은 예제에서도 validation을 밖으로 빼는 순간 계층 경계가 생긴다 | 실패 경로를 status code로 분리해야 한다 |
| 3 | Phase 3 | 400/404/415를 구분된 HTTP 계약으로 고정한다 | `node/src/app.ts`, `node/tests/app.test.ts` | 성공 CRUD만 되면 기본기 연습으로는 충분하다고 느끼기 쉽다 | wrong `Content-Type`, malformed JSON, invalid payload, missing book을 다른 status code로 돌려줬다 | `COREPACK_ENABLE_AUTO_PIN=0 pnpm run test` | health, create/fetch, invalid payload, wrong content-type 4개 시나리오가 모두 통과한다 | `sendJson(response, 415, { message: "content-type must be application/json" })` | HTTP 기본기는 성공 응답보다 실패를 어떤 code로 나누는지에서 더 잘 드러난다 | 다음 프로젝트에서 같은 CRUD를 Express와 NestJS로 비교한다 |

## 근거 파일

- `bridge/02-http-and-api-basics/README.md`
- `bridge/02-http-and-api-basics/problem/README.md`
- `bridge/02-http-and-api-basics/node/src/app.ts`
- `bridge/02-http-and-api-basics/node/src/book-store.ts`
- `bridge/02-http-and-api-basics/node/tests/app.test.ts`
