# 02-http-and-api-basics structure plan

## 중심 질문

- frameworkless HTTP 서버에서 어떤 책임을 직접 들고 가야 했는가
- `BookStore`와 request handler를 왜 분리했는가
- `400`, `404`, `415`를 나누는 순간이 왜 다음 REST 프로젝트의 준비가 되는가

## 10-development-timeline.md

- 오프닝: 이 프로젝트가 "HTTP를 프레임워크 없이 손으로 만져 보는 브리지"라는 점을 먼저 세운다.
- Phase 1: `BookStore`와 payload validator로 도메인 규칙을 먼저 분리한 장면.
- Phase 2: `readJsonBody()`, `sendJson()`, `matchBookId()`와 `createApp()`가 route와 body parsing을 직접 처리하는 장면.
- Phase 3: test가 성공 CRUD와 실패 status code를 함께 고정하는 장면.
- 강조 포인트: 이 프로젝트의 성과는 CRUD 자체보다 "프레임워크가 숨기는 기본 HTTP 책임을 직접 본다"는 데 있다.
