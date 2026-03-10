# 04 IAM Policy Analyzer notion 기록

## 이 문서 묶음이 하는 일

이 `notion/`은 과제 01의 policy evaluation 결과를 운영자가 읽는 finding 구조로 확장하는 과정을 정리합니다.
현재 버전은 analyzer 코드와 테스트가 실제로 보장하는 broad permission, escalation risk, zero-finding safe policy 세 축을 중심으로 다시 썼습니다.

## 이 문서를 읽을 때 잡아야 할 질문

- 왜 broad admin과 `iam:PassRole` 위험을 같은 finding으로 묶지 않았는가?
- 왜 safe policy에서 0건이 나오는 테스트가 analyzer 품질의 핵심 근거인가?
- 이 finding 구조가 왜 remediation과 control plane에서도 유지돼야 하는가?

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
- 구현 진입점: [../python/src/iam_policy_analyzer/analyzer.py](../python/src/iam_policy_analyzer/analyzer.py)
- CLI 진입점: [../python/src/iam_policy_analyzer/cli.py](../python/src/iam_policy_analyzer/cli.py)
- 검증 코드: [../python/tests/test_analyzer.py](../python/tests/test_analyzer.py)
- 이전 장문 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
