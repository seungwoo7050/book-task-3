# 06 Remediation Pack Runner 구조 메모

이 문서는 최종 글을 쓰기 전에 서사 배치를 점검하는 메모다. 독자에게 무엇을 먼저 설명하고 어디서 코드와 CLI를 꺼내 올지 한눈에 보이도록 정리한다.

## 이번 문서가 맡는 일
- finding을 즉시 실행하는 자동화가 아니라, 사람이 검토 가능한 remediation plan으로 바꾸는 프로젝트로 서사를 잡는다.
- 본문은 `출력 shape -> control별 mode 분기 -> approval 상태 전이` 순서로 배치해 안전장치를 먼저 보이게 한다.

## 먼저 붙들 소스 묶음
- [`../../../01-cloud-security-core/06-remediation-pack-runner/README.md`](../../../01-cloud-security-core/06-remediation-pack-runner/README.md)
- [`../../../01-cloud-security-core/06-remediation-pack-runner/problem/README.md`](../../../01-cloud-security-core/06-remediation-pack-runner/problem/README.md)
- [`../../../01-cloud-security-core/06-remediation-pack-runner/docs/concepts/dry-run-remediation.md`](../../../01-cloud-security-core/06-remediation-pack-runner/docs/concepts/dry-run-remediation.md)
- [`../../../01-cloud-security-core/06-remediation-pack-runner/python/README.md`](../../../01-cloud-security-core/06-remediation-pack-runner/python/README.md)
- [`../../../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/runner.py`](../../../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/runner.py)
- [`../../../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/cli.py`](../../../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/cli.py)
- [`../../../01-cloud-security-core/06-remediation-pack-runner/python/tests/test_runner.py`](../../../01-cloud-security-core/06-remediation-pack-runner/python/tests/test_runner.py)

## 본문을 배치하는 순서

- `00-series-map.md`
  - finding control ID와 remediation plan 사이의 계약을 먼저 설명한다.
- `10-development-timeline.md`
  - 도입: 보안 자동화에서 왜 즉시 적용보다 dry-run plan이 먼저여야 하는지 시작점으로 둔다.
  - Phase 1. remediation 출력 shape부터 고정했다.
  - Phase 2. remediation mode를 control별로 갈랐다.
  - Phase 3. approval 상태 전이를 별도 함수로 분리했다.
  - 마무리: capstone worker가 이 status transition을 어떻게 재사용하는지 넘긴다.

## 강조할 코드와 CLI
- 코드 앵커: `RemediationPlan`, control-to-mode mapping, approval helper, CLI render path
- CLI 앵커: `python -m remediation_pack_runner.cli ...`, `pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests`
- 개념 훅: remediation 시스템의 핵심은 실행 자체보다 실행 전후 상태를 추적 가능한 데이터로 두는 데 있다는 점

## 리라이트 기준
- chronology는 실제 commit timestamp보다 source, test, CLI가 묶이는 순서를 기준으로 읽는다.
- 이 문서는 메타 기록보다 서사 배치와 강조점에 집중한다.
