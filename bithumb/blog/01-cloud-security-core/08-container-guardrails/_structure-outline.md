# 08 Container Guardrails 구조 메모

이 문서는 최종 글을 쓰기 전에 서사 배치를 점검하는 메모다. 독자에게 무엇을 먼저 설명하고 어디서 코드와 CLI를 꺼내 올지 한눈에 보이도록 정리한다.

## 이번 문서가 맡는 일
- Kubernetes manifest와 image metadata를 읽어 클러스터 없이도 설명 가능한 guardrail scanner를 세우는 흐름을 복원한다.
- 서사는 `manifest 위험 신호 -> securityContext privilege 신호 -> image metadata와 secure fixture` 순으로 간다.

## 먼저 붙들 소스 묶음
- [`../../../01-cloud-security-core/08-container-guardrails/README.md`](../../../01-cloud-security-core/08-container-guardrails/README.md)
- [`../../../01-cloud-security-core/08-container-guardrails/problem/README.md`](../../../01-cloud-security-core/08-container-guardrails/problem/README.md)
- [`../../../01-cloud-security-core/08-container-guardrails/docs/concepts/container-guardrails.md`](../../../01-cloud-security-core/08-container-guardrails/docs/concepts/container-guardrails.md)
- [`../../../01-cloud-security-core/08-container-guardrails/python/README.md`](../../../01-cloud-security-core/08-container-guardrails/python/README.md)
- [`../../../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/scanner.py`](../../../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/scanner.py)
- [`../../../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/cli.py`](../../../01-cloud-security-core/08-container-guardrails/python/src/container_guardrails/cli.py)
- [`../../../01-cloud-security-core/08-container-guardrails/python/tests/test_scanner.py`](../../../01-cloud-security-core/08-container-guardrails/python/tests/test_scanner.py)

## 본문을 배치하는 순서

- `00-series-map.md`
  - manifest와 image metadata를 하나의 guardrail 프로젝트로 묶는 이유를 설명한다.
- `10-development-timeline.md`
  - 도입: 런타임 cluster access 없이도 어떤 설정이 위험한지 설명할 수 있어야 한다는 문제로 시작한다.
  - Phase 1. manifest에서 설명 가능한 위험 설정을 먼저 골랐다.
  - Phase 2. securityContext를 broad privilege 신호로 묶었다.
  - Phase 3. image metadata와 secure fixture 0건으로 경계를 닫았다.
  - 마무리: control plane의 k8s ingestion이 왜 이 static scanner를 재사용하는지 넘긴다.

## 강조할 코드와 CLI
- 코드 앵커: manifest traversal, `latest`/`hostPath`/`privileged`/`runAsRoot`/capability detection, image metadata branch, secure fixture assertions
- CLI 앵커: `python -m container_guardrails.cli ...`, `pytest 01-cloud-security-core/08-container-guardrails/python/tests`
- 개념 훅: container guardrail의 가치는 클러스터를 붙이기 전에 “설명 가능한 위험 설정”을 먼저 고정하는 데 있다는 점

## 리라이트 기준
- chronology는 실제 commit timestamp보다 source, test, CLI가 묶이는 순서를 기준으로 읽는다.
- 이 문서는 메타 기록보다 서사 배치와 강조점에 집중한다.
