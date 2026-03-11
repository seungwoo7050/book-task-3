# 05 CSPM Rule Engine notion 기록

## 이 문서 묶음의 위치

프로젝트 개요는 [../README.md](../README.md)에서 먼저 보고, 이 문서 묶음은 현재 규칙을 어떤 근거로 설계했는지,
어떻게 재현하고 어디서 막혔는지를 보완하는 레이어로 읽습니다.

## 이 문서 묶음이 보완하는 것

이 `notion/`은 CSPM을 막연한 제품명이 아니라, plan JSON과 운영 snapshot을 읽어 설명 가능한 finding을 내는 작은 규칙 엔진으로 재구성한 기록입니다.
학습 재현성 관점에서 가장 중요한 문서는 [05-reproduction-guide.md](05-reproduction-guide.md)입니다. 이 문서는 insecure/secure 비교, access key aging, 테스트 기준을 한 번에 다시 따라갈 수 있게 설계했습니다.

## 이 문서를 읽을 때 잡아야 할 질문

- 왜 plan JSON과 access key snapshot을 함께 읽어야 실제 CSPM에 가까워지는가?
- 좋은 rule은 “많이 잡는 규칙”이 아니라 “secure fixture에서 조용히 통과하는 규칙”이라는 점을 어떻게 증명할 수 있는가?
- finding이 remediation으로 이어지려면 어떤 필드를 반드시 갖고 있어야 하는가?

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
- 구현 진입점: [../python/src/cspm_rule_engine/scanner.py](../python/src/cspm_rule_engine/scanner.py)
- CLI 진입점: [../python/src/cspm_rule_engine/cli.py](../python/src/cspm_rule_engine/cli.py)
- 검증 코드: [../python/tests/test_scanner.py](../python/tests/test_scanner.py)
- 이전 장문 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)
