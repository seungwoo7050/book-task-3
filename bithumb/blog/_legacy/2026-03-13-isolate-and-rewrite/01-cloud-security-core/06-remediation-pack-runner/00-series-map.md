# 06 Remediation Pack Runner - Series Map

이 시리즈는 `notion/` 없이 `README.md`, `problem/README.md`, `python/README.md`, `runner.py`, `cli.py`, `test_runner.py`, 실제 재검증 명령만으로 다시 읽은 학습 로그입니다.

## 이 시리즈가 답하는 질문

- finding 이후 조치안을 어떻게 바로 실행이 아니라 dry-run remediation plan으로 설명할까
- 자동 패치 가능 케이스와 사람 승인 중심 케이스를 어떤 경계로 나눌까

## 실제 구현 표면

- `control_id`에 따라 remediation mode를 `auto_patch_available`, `manual_approval_required`, `manual_review`로 나눕니다.
- 출력은 patch 초안이나 CLI 명령을 포함한 `RemediationPlan` JSON입니다.
- 승인 단계는 plan 자체를 다시 만들어 `status=approved`로 바꾸는 간단한 흐름으로 유지합니다.

## 대표 검증 엔트리

- `PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m remediation_pack_runner.cli 01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json`
- `PYTHONPATH=01-cloud-security-core/06-remediation-pack-runner/python/src .venv/bin/python -m pytest 01-cloud-security-core/06-remediation-pack-runner/python/tests`

## 읽는 순서

1. [프로젝트 README](../../../01-cloud-security-core/06-remediation-pack-runner/README.md)
2. [문제 정의](../../../01-cloud-security-core/06-remediation-pack-runner/problem/README.md)
3. [실행 진입점](../../../01-cloud-security-core/06-remediation-pack-runner/python/README.md)
4. [대표 테스트](../../../01-cloud-security-core/06-remediation-pack-runner/python/tests/test_runner.py)
5. [핵심 구현](../../../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/runner.py)
6. [개발 타임라인](10-development-timeline.md)

## 근거 파일

- [README.md](../../../01-cloud-security-core/06-remediation-pack-runner/README.md)
- [problem/README.md](../../../01-cloud-security-core/06-remediation-pack-runner/problem/README.md)
- [python/README.md](../../../01-cloud-security-core/06-remediation-pack-runner/python/README.md)
- [runner.py](../../../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/runner.py)
- [cli.py](../../../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/cli.py)
- [test_runner.py](../../../01-cloud-security-core/06-remediation-pack-runner/python/tests/test_runner.py)

## Git Anchor

- `2026-03-10 a4b4aae docs: enhance bithumb`
- `2026-03-11 a9c65b3 Track 2에 대한 전반적인 개선 완료 (infobank, bithumb, game-server)`
