# 지식 인덱스

- 개념 문서: [../docs/concepts/consolidated-remediation-workflow.md](../docs/concepts/consolidated-remediation-workflow.md)
- 데모 안내: [../docs/demo-walkthrough.md](../docs/demo-walkthrough.md)
- 문제 정의: [../problem/README.md](../problem/README.md)
- 구현 진입점: [../python/src/collab_saas_security_review/review.py](../python/src/collab_saas_security_review/review.py)
- CLI: [../python/src/collab_saas_security_review/cli.py](../python/src/collab_saas_security_review/cli.py)
- 테스트: [../python/tests/test_review.py](../python/tests/test_review.py), [../python/tests/test_cli.py](../python/tests/test_cli.py)
- `CRYPTO-001`: plain hash는 integrity summary일 뿐 shared-secret authentication이 아니다.
- `AUTH-003`: JWT는 signature 검증만으로 충분하지 않고 issuer, audience, algorithm pinning이 함께 필요하다.
- `OWASP-003`: outbound fetch는 allowlist와 private IP block을 같이 생각해야 SSRF 설명이 닫힌다.
- dependency triage: severity보다 reachable/runtime/direct 여부가 실제 우선순위를 크게 바꾼다.
- remediation board: 서로 다른 finding 타입을 하나의 `P1`~`P4` 언어로 정렬해 주는 통합 표면이다.
