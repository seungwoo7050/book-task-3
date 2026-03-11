# arenaserv 학습 로그

이 폴더는 simulation을 실제 TCP 서버로 올리며 생긴 판단과 실패 사례를 남기는 현재판 로그다. 문제와 범위 요약은 [../README.md](../README.md)에서 먼저 확인한다.

## 읽는 순서

1. [00-problem-framing.md](00-problem-framing.md)
2. [01-approach-log.md](01-approach-log.md)
3. [02-debug-log.md](02-debug-log.md)
4. [03-retrospective.md](03-retrospective.md)
5. [04-knowledge-index.md](04-knowledge-index.md)

## 사용 기준

- ticklab에서 무엇을 가져왔는지는 00, 01에서 본다.
- queue/rejoin/snapshot 실패 사례는 02에서 본다.
- capstone 의미와 비교 포인트는 03, 04에서 본다.
