# 재현 가이드

## 무엇을 재현하나

- manifest와 image metadata를 함께 읽어 guardrail finding을 만드는지
- insecure 입력에서 여덟 개 control이 모두 재현되는지
- secure 입력이 0건으로 통과해 오탐 기준이 유지되는지

## 사전 조건

- `python3` 3.13+와 `make venv`가 필요합니다.
- 명령은 모두 레포 루트에서 실행합니다.

## 가장 짧은 재현 경로

```bash
make venv
PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m container_guardrails.cli scan 01-cloud-security-core/08-container-guardrails/problem/data/insecure_k8s.yaml 01-cloud-security-core/08-container-guardrails/problem/data/insecure_image.json
PYTHONPATH=01-cloud-security-core/08-container-guardrails/python/src .venv/bin/python -m pytest 01-cloud-security-core/08-container-guardrails/python/tests
```

## 기대 결과

- CLI JSON에는 `K8S-001`~`K8S-005`, `IMG-001`~`IMG-003` control이 모두 포함돼야 합니다.
- pytest는 2개 테스트를 통과해야 하며, insecure 입력은 여덟 건, secure 입력은 0건을 검증합니다.
- secure 입력에서 결과가 비어 있지 않다면 guardrail precision이 깨진 것입니다.

## 결과가 다르면 먼저 볼 파일

- scanner 구현을 다시 보려면: [../python/src/container_guardrails/scanner.py](../python/src/container_guardrails/scanner.py)
- CLI 진입 흐름을 다시 보려면: [../python/src/container_guardrails/cli.py](../python/src/container_guardrails/cli.py)
- 입력 fixture를 다시 보려면: [../problem/data/](../problem/data/)
- 검증 기준을 다시 보려면: [../python/tests/test_scanner.py](../python/tests/test_scanner.py)
- 루트 공통 검증 흐름을 다시 보려면: [../../../Makefile](../../../Makefile)

## 이 재현이 증명하는 것

- 이 재현은 cluster 없이도 설명 가능한 컨테이너 보안 규칙을 충분히 학습할 수 있다는 점을 보여 줍니다.
- 학습자는 각 control 이름보다, 왜 manifest와 image를 분리해서 읽는지 먼저 설명할 수 있어야 합니다.
