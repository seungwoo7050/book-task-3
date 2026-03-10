# 01 AWS Security Primitives notion 기록

## 이 문서 묶음이 하는 일

이 `notion/`은 IAM policy evaluation을 단순한 allow/deny 결과가 아니라, 왜 그런 결론이 나왔는지 설명 가능한 판단 흐름으로 정리한 기록입니다.
archive의 장문 설명은 [../notion-archive/essay.md](../notion-archive/essay.md)와 [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)에 남겨 두고, 현재 버전은 엔진 코드·테스트·문제 문서를 근거로 다시 썼습니다.

## 이 문서를 읽을 때 잡아야 할 질문

- 어떤 statement가 매칭됐는지까지 설명하지 않으면 왜 학습 가치가 떨어지는가?
- `explicit deny > allow > implicit deny`를 가장 작은 코드로 어떻게 증명할 수 있는가?
- 이 엔진이 뒤의 IAM analyzer와 control plane에서 어떤 재사용 가치를 가지는가?

## 추천 읽기 순서

학습자가 가장 빨리 손에 잡히는 재현 경로를 보려면 `05-reproduction-guide.md`를 초반에 읽는 편이 좋습니다.

1. [00-problem-framing.md](00-problem-framing.md): 문제와 경계를 먼저 확인합니다.
2. [05-reproduction-guide.md](05-reproduction-guide.md): 가장 짧은 재현 경로와 기대 결과를 확인합니다.
3. [01-approach-log.md](01-approach-log.md): 현재 구현 방향을 왜 택했는지 읽습니다.
4. [02-debug-log.md](02-debug-log.md): 어디서 자주 막히는지와 어떤 테스트가 근거인지 확인합니다.
5. [03-retrospective.md](03-retrospective.md): 지금 구현이 무엇을 증명했고 무엇을 의도적으로 비워 두었는지 읽습니다.
6. [04-knowledge-index.md](04-knowledge-index.md): 다음 프로젝트로 이어지는 개념과 근거 파일을 모아 봅니다.

## 이 버전의 근거

- 현재 문제 설명: [../problem/README.md](../problem/README.md)
- 현재 구현 안내: [../python/README.md](../python/README.md)
- 실제 검증 코드: [../python/tests/test_engine.py](../python/tests/test_engine.py)
- 구현 진입점: [../python/src/aws_security_primitives/engine.py](../python/src/aws_security_primitives/engine.py)
- 이전 장문 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)
