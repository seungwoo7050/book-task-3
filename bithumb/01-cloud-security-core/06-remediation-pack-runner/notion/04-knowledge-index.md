# 지식 인덱스

## 이번 프로젝트에서 굳혀야 할 개념

- remediation은 실행보다 제안이 먼저일 수 있습니다.
- `control_id`는 조치안 종류를 선택하는 가장 작은 routing key입니다.
- approval 전/후 상태를 따로 남겨야 audit가 가능합니다.
- 학습 초반에는 문자열 기반 patch 초안만으로도 충분한 가치가 있습니다.

## 로컬 근거 파일

- 개념 요약: [../docs/concepts/dry-run-remediation.md](../docs/concepts/dry-run-remediation.md)
- 구현 진입점: [../python/src/remediation_pack_runner/runner.py](../python/src/remediation_pack_runner/runner.py)
- CLI 진입점: [../python/src/remediation_pack_runner/cli.py](../python/src/remediation_pack_runner/cli.py)
- 검증 코드: [../python/tests/test_runner.py](../python/tests/test_runner.py)
- 샘플 finding: [../problem/data/sample_finding.json](../problem/data/sample_finding.json)

## 재현 체크포인트

- `sample_finding.json`을 넣었을 때 `mode`가 `auto_patch_available`인지 확인합니다.
- patch 초안 안에 `block_public_acls`가 들어 있어야 public access remediation 맥락이 유지됩니다.
- approval 이후 `status`가 `approved`로 바뀌고 summary에 승인자가 남는지 확인합니다.

## 다음 프로젝트로 이어지는 질문

- `09-exception-and-evidence-manager`는 remediation과 함께 설명되어야 하는 거버넌스 흐름을 보강합니다.
- `10-cloud-security-control-plane`은 remediation 요청과 worker 흐름으로 이 모델을 통합합니다.

## 참고 자료

- 공식 링크 정리: [../docs/references/README.md](../docs/references/README.md)
- 이전 서술형 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)
