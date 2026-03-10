# 08 Container Guardrails notion 기록

## 이 문서 묶음이 하는 일

이 `notion/`은 EKS 클러스터 없이도 컨테이너 보안의 핵심 guardrail을 학습할 수 있다는 점을 보여 주는 기록입니다.
현재 버전은 manifest scanner, image metadata scanner, insecure/secure fixture 쌍과 테스트가 실제로 증명하는 여덟 개 control을 중심으로 다시 정리했습니다.

## 이 문서를 읽을 때 잡아야 할 질문

- 왜 manifest만으로도 충분히 배울 수 있는 보안 규칙이 많은가?
- image metadata와 manifest는 어떤 다른 시점의 증거인가?
- secure fixture 0건이 왜 guardrail 문서에서 핵심 근거인가?

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
- 구현 진입점: [../python/src/container_guardrails/scanner.py](../python/src/container_guardrails/scanner.py)
- CLI 진입점: [../python/src/container_guardrails/cli.py](../python/src/container_guardrails/cli.py)
- 검증 코드: [../python/tests/test_scanner.py](../python/tests/test_scanner.py)
- 입력 fixture: [../problem/data/](../problem/data/)
- 이전 장문 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
