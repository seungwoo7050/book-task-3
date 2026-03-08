# Node Implementation

## 범위

Node 기본 HTTP 서버와 간단한 in-memory API를 제공한다.

## 현재 상태

- 상태: `verified`
- build: `pnpm run build`
- test: `pnpm run test`
- run: `pnpm start`

## 포함된 것

- `src/app.ts`: 라우팅과 본문 파싱이 들어 있는 HTTP 서버
- `src/book-store.ts`: in-memory 저장소
- `tests/app.test.ts`: CRUD와 오류 응답 검증

## 알려진 제약

- 학습용 구현이라 persistence, pagination, 인증은 다루지 않는다.
