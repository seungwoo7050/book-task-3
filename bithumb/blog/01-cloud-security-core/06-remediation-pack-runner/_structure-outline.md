# 06 Remediation Pack Runner 구조 메모

## 이번 문서의 중심
- remediation을 "실행기"로 과장하지 않는다.
- 서사는 `plan 계약 -> control별 조치 강도 분류 -> approval 상태 전이` 순서로 고정한다.
- README 설명보다 실제 코드 인터페이스가 더 중요하다는 점을 한 번 짚는다.

## 먼저 붙들 소스
- `../../../01-cloud-security-core/06-remediation-pack-runner/README.md`
- `../../../01-cloud-security-core/06-remediation-pack-runner/problem/README.md`
- `../../../01-cloud-security-core/06-remediation-pack-runner/python/README.md`
- `../../../01-cloud-security-core/06-remediation-pack-runner/docs/concepts/dry-run-remediation.md`
- `../../../01-cloud-security-core/06-remediation-pack-runner/problem/data/sample_finding.json`
- `../../../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/runner.py`
- `../../../01-cloud-security-core/06-remediation-pack-runner/python/src/remediation_pack_runner/cli.py`
- `../../../01-cloud-security-core/06-remediation-pack-runner/python/tests/test_runner.py`

## 본문 배치
- 도입
  - finding을 바로 apply하지 않고 plan으로 멈춰 세우는 이유를 먼저 둔다.
- Phase 1
  - `RemediationPlan`과 sample fixture로 입력/출력 계약을 고정한다.
- Phase 2
  - `CSPM-001`, `CSPM-002`, fallback을 서로 다른 운영 모드로 나누는 장면을 중심에 둔다.
  - pytest가 덮지 않는 branch는 보조 재실행으로 확인했다는 점을 같이 적는다.
- Phase 3
  - `approve()`가 실제 실행이 아니라 승인 표지만 바꾼다는 점을 보여 준다.
- 마무리
  - apply/rollback/approval system이 아직 바깥 책임이라는 한계를 분명히 남긴다.

## 꼭 남길 검증 신호
- CLI 단일 입력 실행 결과에서 `auto_patch_available`, `pending_approval`, patch snippet 확인
- 보조 Python 재실행에서 `manual_approval_required`, `manual_review` 확인
- pytest `2 passed in 0.01s`
- README 예시와 달리 실제 CLI는 서브커맨드 없이 호출된다는 점

## 탈락 기준
- README를 풀어쓴 수준으로 끝나면 안 된다.
- approval을 완전한 워크플로처럼 과장하면 안 된다.
- 테스트가 덮지 않는 분기를 마치 자동으로 보장된 것처럼 쓰면 안 된다.
