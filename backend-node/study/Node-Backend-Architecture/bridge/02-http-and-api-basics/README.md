# 02-http-and-api-basics

- 그룹: `Bridge`
- 상태: `verified`
- 공개 답안 레인: `node/`
- 성격: 신규 설계

## 한 줄 문제

프레임워크를 쓰기 전에 HTTP 요청/응답, status code, JSON 직렬화를 직접 구현하며 API의 최소 단위를 익히는 문제다.

## 성공 기준

- frameworkless HTTP 서버에서 route, body parsing, status code를 직접 처리할 수 있다.
- JSON 요청/응답과 `Content-Type` 오류를 테스트로 고정할 수 있다.
- Express/NestJS로 넘어가기 전 HTTP 계약을 코드와 테스트 양쪽에서 설명할 수 있다.

## 내가 만든 답

- `node/`에 in-memory Books HTTP 서버와 검증 테스트를 만들었다.
- `415`, `400`, `404` 같은 기본 실패 경로를 명시적으로 다뤘다.
- 후속 REST 프로젝트에서 프레임워크가 가리는 부분을 먼저 손으로 경험하게 했다.

## 제공 자료

- `problem/README.md`
- `node/`
- `docs/`
- `notion/`

## 실행과 검증

### Node HTTP 구현
- 작업 디렉터리: `node/`
- install: `pnpm install`
- verify: `pnpm run build && pnpm run test`
- run: `pnpm start`

## 왜 다음 단계로 이어지는가

- `03-rest-api-foundations`에서 같은 CRUD 문제를 Express와 NestJS 두 레인으로 분해해 비교한다.
- canonical problem statement는 [problem/README.md](problem/README.md)에서, 구현별 실행 메모는 [node/README.md](node/README.md)에서 확인한다.
