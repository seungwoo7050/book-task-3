# 02-http-and-api-basics structure plan

이 문서는 "프레임워크 없이도 서버가 돈다"는 감상보다, HTTP의 최소 계약을 손으로 구현했을 때 무엇이 드러나는지 보여 줘야 한다. 중심축은 `server skeleton -> in-memory store -> status code contract`다.

## 읽기 구조

1. `app.ts`에서 직접 body를 읽고 route를 나누는 장면으로 시작한다.
2. `BookStore`와 validator를 분리한 이유를 짧게 잡는다.
3. `400/404/415`를 나눈 실패 경로를 마지막 전환점으로 둔다.

## 반드시 남길 근거

- `readJsonBody`
- `sendJson`
- `BookStore`
- `validateCreateBookPayload`
- invalid JSON / wrong `Content-Type` 처리
- `pnpm run build`
- `pnpm run test`

## 리라이트 톤

- 프레임워크가 없어서 불편했다는 인상보다, 프레임워크가 자동으로 하던 일이 무엇인지 손에 잡히게 쓴다.
- 성공 CRUD보다 실패 경로가 왜 더 설명력이 큰지 드러낸다.
