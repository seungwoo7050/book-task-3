# Checked Sources

- Node.js API: `http`
  - checked: 2026-03-07
  - why: `createServer`, `IncomingMessage`, `ServerResponse`의 최소 사용법을 다시 확인했다.
  - learned: 초보 단계에서는 프레임워크보다 HTTP 기본 객체를 먼저 보는 편이 후속 학습의 마찰을 줄인다.
- MDN HTTP response status codes
  - checked: 2026-03-07
  - why: `400`, `404`, `415`를 어떤 조건에서 나눌지 정리했다.
  - learned: 오류 응답을 세분화해야 테스트가 "왜 실패했는지"를 설명할 수 있다.
