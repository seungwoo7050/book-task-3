# 09 Exception and Evidence Manager 구조 메모

이 문서는 최종 글을 쓰기 전에 서사 배치를 점검하는 메모다. 독자에게 무엇을 먼저 설명하고 어디서 코드와 CLI를 꺼내 올지 한눈에 보이도록 정리한다.

## 이번 문서가 맡는 일
- exception, evidence, audit를 단순 보조 데이터가 아니라 서로 다른 governance record로 모델링하는 과정을 보여 준다.
- 글은 `record 분리 -> suppression rule -> append-only evidence/audit` 순서로 배치한다.

## 먼저 붙들 소스 묶음
- [`../../../01-cloud-security-core/09-exception-and-evidence-manager/README.md`](../../../01-cloud-security-core/09-exception-and-evidence-manager/README.md)
- [`../../../01-cloud-security-core/09-exception-and-evidence-manager/problem/README.md`](../../../01-cloud-security-core/09-exception-and-evidence-manager/problem/README.md)
- [`../../../01-cloud-security-core/09-exception-and-evidence-manager/docs/concepts/governance-flow.md`](../../../01-cloud-security-core/09-exception-and-evidence-manager/docs/concepts/governance-flow.md)
- [`../../../01-cloud-security-core/09-exception-and-evidence-manager/python/README.md`](../../../01-cloud-security-core/09-exception-and-evidence-manager/python/README.md)
- [`../../../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/manager.py`](../../../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/manager.py)
- [`../../../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/cli.py`](../../../01-cloud-security-core/09-exception-and-evidence-manager/python/src/exception_evidence_manager/cli.py)
- [`../../../01-cloud-security-core/09-exception-and-evidence-manager/python/tests/test_manager.py`](../../../01-cloud-security-core/09-exception-and-evidence-manager/python/tests/test_manager.py)

## 본문을 배치하는 순서

- `00-series-map.md`
  - 왜 governance flow가 별도 독립 프로젝트인지, 어떤 상태 전이가 핵심인지 먼저 고정한다.
- `10-development-timeline.md`
  - 도입: finding suppression을 bool flag 하나로 두면 안 되는 이유에서 시작한다.
  - Phase 1. 예외와 증적과 감사를 record로 분리했다.
  - Phase 2. approval과 expiry를 suppression 판정에 연결했다.
  - Phase 3. evidence append와 append-only audit trail을 잠갔다.
  - 마무리: capstone DB 모델이 이 구조를 어떻게 흡수하는지 질문으로 넘긴다.

## 강조할 코드와 CLI
- 코드 앵커: exception/evidence/audit dataclass, approval/expiry suppression helper, append-only audit append, CLI render path
- CLI 앵커: `python -m exception_evidence_manager.cli ...`, `pytest 01-cloud-security-core/09-exception-and-evidence-manager/python/tests`
- 개념 훅: governance에서 중요한 것은 상태값 하나가 아니라 “누가, 언제, 어떤 근거로 억제했는가”를 별도 record로 남기는 것이라는 점

## 리라이트 기준
- chronology는 실제 commit timestamp보다 source, test, CLI가 묶이는 순서를 기준으로 읽는다.
- 이 문서는 메타 기록보다 서사 배치와 강조점에 집중한다.
