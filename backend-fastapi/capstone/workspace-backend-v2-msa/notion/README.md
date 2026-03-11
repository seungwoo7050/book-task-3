# workspace-backend-v2-msa 학습 로그

이 폴더는 workspace-backend-v2-msa의 현재 공개용 학습 로그입니다. 설계 문서가 답의 구조를 설명한다면, 여기서는 구현 순서, 실패 사례, 재현 경로를 기록합니다.

이 폴더는 v1 기준선에서 v2 MSA로 재편하는 과정을 공개용 학습 노트로 정리한 세트다. 단순 구현 기록이 아니라, 왜 이 분해를 택했고 어떤 비용을 치렀는지까지 추적하는 데 목적이 있다.

## 이 폴더의 역할

- 구현 순서와 의사결정 압축본을 남깁니다.
- 실패 사례와 수정 근거를 기록합니다.
- 다음에 다시 만들 때 따라갈 재현 순서를 제공합니다.

## 추천 읽기 순서

1. [00-problem-framing.md](00-problem-framing.md)
2. [01-approach-log.md](01-approach-log.md)
3. [02-debug-log.md](02-debug-log.md)
4. [03-retrospective.md](03-retrospective.md)
5. [04-knowledge-index.md](04-knowledge-index.md)
6. [05-development-timeline.md](05-development-timeline.md)

## 목적별로 읽는 방법

- 바로 다시 실행하고 싶다면 [05-development-timeline.md](05-development-timeline.md)부터 봅니다.
- 왜 이런 구조를 택했는지 따라가고 싶다면 `00`, `01`부터 읽습니다.
- 실제로 부딪힌 실패와 수정 근거를 보고 싶다면 `02`를 봅니다.
- 포트폴리오 확장 아이디어가 필요하면 `03`, `04`를 봅니다.
