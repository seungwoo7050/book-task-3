# eventlab series map

`eventlab`을 세 편으로 나눈 이유는 기능 목록을 잘라 놓기 위해서가 아니다. 이 lab은 작은 대신, 뒤의 모든 서버 문서가 재사용할 runtime 감각을 먼저 만들어 준다. 그래서 시리즈도 "event loop 뼈대 -> line protocol과 keep-alive -> 실제 검증과 경계" 순서로 읽히도록 나눴다.

첫 글은 서버가 어떤 순서로만 움직이게 만들었는지에 집중한다. 둘째 글은 그 뼈대 위에 `PING`/`PONG`, `ECHO`, idle keep-alive 같은 최소 계약이 어떻게 올라가는지 다룬다. 마지막 글은 smoke test가 무엇을 진짜로 증명하는지, 그리고 parser나 상태 전이 같은 문제는 왜 아직 일부러 남겨 두는지를 정리한다.

## 글 순서

1. [10-runtime-surface-and-event-loop.md](10-runtime-surface-and-event-loop.md)
2. [20-line-protocol-and-keepalive.md](20-line-protocol-and-keepalive.md)
3. [30-smoke-verification-and-boundaries.md](30-smoke-verification-and-boundaries.md)

