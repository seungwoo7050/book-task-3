# 07 Security Lake Mini notion 기록

## 이 문서 묶음의 위치

프로젝트 개요는 [../README.md](../README.md)에서 먼저 보고, 이 문서 묶음은 현재 detection query와 lake 구조를 왜 그렇게
잡았는지, 어떻게 재현하고 어디서 막혔는지를 보완하는 레이어로 읽습니다.

## 이 문서 묶음이 보완하는 것

이 `notion/`은 로그를 적재하는 단계 위에 detection query를 얹어, alert 생성까지 이어지는 작은 security lake 흐름을 설명합니다.
현재 버전은 `lake.py`, suspicious CloudTrail fixture, 테스트가 실제로 보장하는 다섯 개 alert를 중심으로 다시 정리했습니다.

## 이 문서를 읽을 때 잡아야 할 질문

- alert는 finding과 무엇이 다른가?
- 왜 detection rule을 SQL처럼 읽히는 구조로 유지하려 했는가?
- 정규화된 CloudTrail 이벤트가 있어야 왜 이 단계가 가능해지는가?

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
- 구현 진입점: [../python/src/security_lake_mini/lake.py](../python/src/security_lake_mini/lake.py)
- CLI 진입점: [../python/src/security_lake_mini/cli.py](../python/src/security_lake_mini/cli.py)
- 검증 코드: [../python/tests/test_lake.py](../python/tests/test_lake.py)
- 입력 fixture: [../problem/data/cloudtrail_suspicious.json](../problem/data/cloudtrail_suspicious.json)
- 이전 장문 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
