# Structure Design — collab-saas-security-review

이 outline는 최종 글이 “통합 데모가 있다”는 요약문에 머물지 않고, why-now가 있는 remediation board가 어떻게 만들어지는지 단계적으로 보여 주도록 설계한 뼈대다.

## opening

- 시작 질문: 왜 capstone은 서버를 띄우는 대신 review bundle과 remediation board에 집중했는가.
- 첫 증거: `docs/concepts/consolidated-remediation-workflow.md`와 `review.py::_build_remediation_board`
- 서술 원칙: 통합 데모라는 말보다 먼저 “같은 priority 언어로 다시 정렬한다”는 설계 의도를 분명히 한다.

## Session 1 — category evaluator를 다시 세웠다

- 다룰 표면: `crypto.py`, `auth.py`, `backend.py`, `dependency.py`
- 먼저 던질 질문: “통합 review도 category별 판단이 먼저 독립적으로 계산돼야 한다.”
- 꼭 넣을 CLI: `PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src .venv/bin/python -m pytest study/90-capstone-collab-saas-security-review/python/tests`
- 꼭 남길 검증 신호: `7 passed in 0.05s`
- 핵심 전환 문장: foundations 패키지를 import하지 않고 vocabulary만 재사용한 선택이 통합 글의 방향을 결정했다.

## Session 2 — remediation board 정렬 규칙을 고정했다

- 다룰 표면: `python/src/collab_saas_security_review/review.py::_normalize_priority`, `_build_remediation_board`, `build_review`
- 먼저 던질 질문: “통합의 핵심은 finding 개수 합계가 아니라 어떤 일을 먼저 해야 하는지 말하는 것이다.”
- 꼭 넣을 CLI: `... cli review ... review_bundle.json`
- 꼭 남길 검증 신호: `remediation_items=21`, 첫 항목 `crypto:CRYPTO-001...`, 마지막 항목 `dependency:CVE-2026-1003:pytest`
- 핵심 전환 문장: `P1 -> P4`, `crypto -> auth -> backend -> dependency` 정렬 규칙이 board를 읽는 법 자체를 만든다.

## Session 3 — artifact와 markdown report를 분리했다

- 다룰 표면: `python/src/collab_saas_security_review/review.py::render_markdown_report`, `write_artifacts`
- 먼저 던질 질문: “JSON 하나만으로는 운영자와 리뷰어가 같은 속도로 읽을 수 없다.”
- 꼭 넣을 CLI: `... cli demo ... demo_bundle.json`
- 꼭 남길 검증 신호: `.artifacts/capstone/demo/01-service-profile.json`부터 `07-report.md`까지 7개 파일 생성
- 핵심 전환 문장: service profile, category findings, remediation board, report를 나누자 review 결과가 역할별로 읽히기 시작했다.

## Session 4 — baseline과 output-dir 계약을 테스트로 닫았다

- 다룰 표면: `python/src/collab_saas_security_review/cli.py`, `python/tests/test_review.py`, `python/tests/test_cli.py`
- 먼저 던질 질문: “통합 리뷰는 취약 bundle뿐 아니라 secure baseline 0건도 같은 contract로 보여 줘야 한다.”
- 꼭 넣을 CLI: `PYTHONPATH=study/90-capstone-collab-saas-security-review/python/src .venv/bin/python -m pytest study/90-capstone-collab-saas-security-review/python/tests`
- 꼭 남길 검증 신호: secure baseline summary 전부 0, artifact 7개, report 섹션 6개
- 핵심 전환 문장: baseline 0건이 있어야 remediation board의 의미가 과장되지 않는다.

## ending

- 마지막 단락에서는 실제 API 호출, queue, DB state transition, 외부 advisory feed 동기화는 현재 범위 밖임을 짧게 남긴다.
- 시리즈의 끝에서는 foundations 프로젝트 네 개가 왜 capstone review vocabulary로 합쳐졌는지 다시 연결한다.
