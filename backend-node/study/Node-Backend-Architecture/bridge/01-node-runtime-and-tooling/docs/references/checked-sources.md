# Checked Sources

- Node.js API: `fs`
  - checked: 2026-03-07
  - why: `createReadStream`과 promise 기반 파일 접근의 역할을 다시 정리했다.
  - learned: 학습용 CLI에서도 동기 I/O보다 스트리밍 I/O를 먼저 보여주는 편이 다음 단계로 연결하기 좋다.
- Node.js API: `readline`
  - checked: 2026-03-07
  - why: NDJSON를 한 줄씩 읽는 가장 단순한 방법을 확인했다.
  - learned: 파싱 실패 줄 번호를 남기면 입력 데이터 문제를 훨씬 빨리 좁힐 수 있다.
