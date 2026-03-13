# Structure Design — owasp-backend-mitigations

이 outline는 최종 글이 OWASP 항목 해설이 아니라 route surface에서 방어 경계가 어떻게 finding으로 바뀌는지 보여 주도록 잡은 뼈대다.

## opening

- 시작 질문: 왜 이 프로젝트는 실제 framework보다 route fixture와 defense vocabulary를 먼저 세웠는가.
- 첫 증거: `docs/concepts/backend-defense-five.md`와 `evaluator.py::CONTROL_META`
- 서술 원칙: OWASP 용어 설명보다 route 입력 경계가 finding으로 바뀌는 장면을 먼저 보여 준다.

## Session 1 — defense vocabulary를 먼저 고정했다

- 다룰 표면: `python/src/owasp_backend_mitigations/evaluator.py`
- 먼저 던질 질문: “backend 보안은 취약점 이름이 아니라 route에서 빠진 방어를 말할 수 있어야 한다.”
- 꼭 넣을 CLI: `PYTHONPATH=study/03-owasp-backend-mitigations/python/src .venv/bin/python -m pytest study/03-owasp-backend-mitigations/python/tests`
- 꼭 남길 검증 신호: `5 passed in 0.03s`
- 핵심 전환 문장: SSRF 분기에서 allowlist와 private IP blocking을 따로 체크한 순간 route defense가 훨씬 구체적으로 보였다.

## Session 2 — case bundle로 반복 가능한 판정을 만들었다

- 다룰 표면: `python/src/owasp_backend_mitigations/cases.py`
- 먼저 던질 질문: “finding 함수가 있어도 어떤 route가 어떤 finding을 가져야 하는지 비교하는 층이 필요하다.”
- 꼭 넣을 CLI: `... cli check-cases ... case_bundle.json`
- 꼭 남길 검증 신호: `passed=6`, `failed=0`
- 핵심 전환 문장: `actual_control_ids == expected_control_ids` 비교가 secure baseline과 negative case를 같은 언어로 묶는다.

## Session 3 — composite demo와 테스트로 마감했다

- 다룰 표면: `python/src/owasp_backend_mitigations/cli.py`, `python/tests/test_cli.py`
- 먼저 던질 질문: “복합 route에서 다섯 finding이 한 번에 터질 때도 vocabulary가 유지되는가.”
- 꼭 넣을 CLI: `... cli demo ... demo_profile.json`
- 꼭 남길 검증 신호: `batch_export_proxy`의 `OWASP-001`~`OWASP-005`
- 핵심 전환 문장: composite demo는 route 하나에 여러 방어 경계가 겹친다는 사실을 한 번에 보여 준다.

## ending

- 마지막 단락에서는 범위 밖인 `XSS`, `deserialization`, `authz-as-code`를 짧게 남긴다.
- 다음 질문은 “route finding을 patch queue와 action 언어로 어떻게 바꿀까”로 넘긴다.
