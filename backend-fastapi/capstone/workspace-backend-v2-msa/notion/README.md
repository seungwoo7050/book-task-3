# workspace-backend-v2-msa 학습 노트

이 폴더는 v1 기준선에서 v2 MSA로 재편하는 과정을 공개용 학습 노트로 정리한 세트다. 단순 구현 기록이 아니라, 왜 이 분해를 택했고 어떤 비용을 치렀는지까지 추적하는 데 목적이 있다.

## 먼저 볼 문서

- 큰 그림부터 보려면 [00-problem-framing.md](00-problem-framing.md)
- 분해 이유와 대안 비교를 보려면 [01-approach-log.md](01-approach-log.md)
- 실제 구현 순서를 따라가려면 [05-development-timeline.md](05-development-timeline.md)

## 추천 읽기 순서

1. [00-problem-framing.md](00-problem-framing.md)
2. [01-approach-log.md](01-approach-log.md)
3. [05-development-timeline.md](05-development-timeline.md)
4. [02-debug-log.md](02-debug-log.md)
5. [03-retrospective.md](03-retrospective.md)
6. [04-knowledge-index.md](04-knowledge-index.md)

## 이 노트 세트에서 특히 봐야 할 것

- v1과 같은 도메인을 유지한 이유
- gateway를 따로 둔 이유
- outbox, stream, pub/sub가 한 흐름 안에서 동시에 필요한 이유
- “설명 가능한 MSA”와 “운영급 MSA” 사이의 경계
