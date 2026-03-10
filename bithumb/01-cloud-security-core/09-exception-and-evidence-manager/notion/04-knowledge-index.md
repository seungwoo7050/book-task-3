# 지식 인덱스

## 이번 프로젝트에서 굳혀야 할 개념

- exception은 finding을 지우는 행위가 아니라 근거 있는 suppression 구조입니다.
- approval, expiry, evidence, audit는 서로 다른 책임을 가지는 개념입니다.
- append-only audit는 규제 대응과 포렌식 관점에서 중요합니다.
- 메모리 모델이어도 핵심 비즈니스 로직을 먼저 고정할 수 있습니다.

## 로컬 근거 파일

- 개념 요약: [../docs/concepts/governance-flow.md](../docs/concepts/governance-flow.md)
- 구현 진입점: [../python/src/exception_evidence_manager/manager.py](../python/src/exception_evidence_manager/manager.py)
- CLI 진입점: [../python/src/exception_evidence_manager/cli.py](../python/src/exception_evidence_manager/cli.py)
- 검증 코드: [../python/tests/test_manager.py](../python/tests/test_manager.py)
- 문제 범위: [../problem/README.md](../problem/README.md)

## 재현 체크포인트

- CLI demo 결과에서 `approved_status`가 `approved`, `audit_event_count`가 `3`인지 확인합니다.
- 테스트에서 expiry 이후 `is_suppressed`가 `False`로 바뀌는지 확인합니다.
- audit event의 첫 항목이 `exception.created`인지 확인해 append-only 흐름이 유지되는지 봅니다.

## 다음 프로젝트로 이어지는 질문

- `10-cloud-security-control-plane`은 같은 개념을 SQLAlchemy와 API로 영속화합니다.
- `06-remediation-pack-runner`와 함께 보면 remediation과 exception이 같은 운영 흐름 안에서 만나는 이유를 설명할 수 있습니다.

## 참고 자료

- 공식 링크 정리: [../docs/references/README.md](../docs/references/README.md)
- 이전 서술형 기록: [../notion-archive/essay.md](../notion-archive/essay.md)
- 이전 작업 로그: [../notion-archive/dev-timeline.md](../notion-archive/dev-timeline.md)
