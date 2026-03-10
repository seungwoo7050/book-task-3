# 재현 가이드

## 무엇을 재현하나

- exception 생성-승인-만료 판단 흐름이 재현되는지
- evidence 첨부와 audit event 누적이 함께 동작하는지
- suppression 상태가 시간이 지나면 자동으로 풀리는지

## 사전 조건

- `python3` 3.13+와 `make venv`가 필요합니다.
- 명령은 모두 레포 루트에서 실행합니다.

## 가장 짧은 재현 경로

```bash
make venv
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m exception_evidence_manager.cli demo
PYTHONPATH=01-cloud-security-core/09-exception-and-evidence-manager/python/src .venv/bin/python -m pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests
```

## 기대 결과

- CLI JSON에는 `approved_status: approved`, `audit_event_count: 3`가 포함돼야 합니다.
- pytest는 2개 테스트를 통과하면서 suppression expiry와 audit append를 함께 검증해야 합니다.
- 첫 audit event는 `exception.created`여야 하며, 승인 후에는 suppression이 true로 바뀌어야 합니다.

## 결과가 다르면 먼저 볼 파일

- 예외 관리 로직을 다시 보려면: [../python/src/exception_evidence_manager/manager.py](../python/src/exception_evidence_manager/manager.py)
- CLI demo 흐름을 다시 보려면: [../python/src/exception_evidence_manager/cli.py](../python/src/exception_evidence_manager/cli.py)
- 검증 기준을 다시 보려면: [../python/tests/test_manager.py](../python/tests/test_manager.py)
- 문제 범위를 다시 보려면: [../problem/README.md](../problem/README.md)
- 루트 공통 검증 흐름을 다시 보려면: [../../../Makefile](../../../Makefile)

## 이 재현이 증명하는 것

- 이 재현은 예외 관리가 “조용히 무시한다”가 아니라, 승인·만료·증거·감사를 갖춘 데이터 흐름이라는 점을 보여 줍니다.
- 학습자는 이 단계에서 suppression과 deletion을 혼동하지 않는 것이 중요합니다.
