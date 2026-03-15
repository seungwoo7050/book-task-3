# security-core 서버 개발 필수 답안지

이 문서는 security-core 필수 과제를 실제 Python source와 테스트만으로 해설하는 답안지다. 핵심은 각 과제가 "보안 도구를 만든다"가 아니라 "판단 기준을 코드로 고정한다"는 점을 읽는 것이다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [02-auth-threat-modeling-python](02-auth-threat-modeling-python_answer.md) | 시작 위치의 구현을 완성해 secure baseline scenario는 0 finding이어야 합니다, insecure scenario는 기대한 AUTH-* control ID만 반환해야 합니다, check-scenarios <manifest>가 시나리오별 matched 여부와 finding 목록을 JSON으로 출력해야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 check_scenarios와 demo, _finding 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test-unit && make demo-auth` |
| [03-owasp-backend-mitigations-python](03-owasp-backend-mitigations-python_answer.md) | 시작 위치의 구현을 완성해 secure baseline case는 0 finding이어야 합니다, insecure case는 기대한 OWASP-* control ID만 반환해야 합니다, check-cases <manifest>가 case별 matched 여부와 finding 목록을 JSON으로 출력해야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 load_json와 check_case_manifest, demo_profile 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test-unit && make demo-owasp` |
| [04-dependency-vulnerability-workflow-python](04-dependency-vulnerability-workflow-python_answer.md) | 시작 위치의 구현을 완성해 각 advisory가 deterministic priority와 action으로 변환되어야 합니다, 각 item의 score와 reason code가 설명 가능해야 합니다, triage <bundle>가 expected item과 실제 결과를 비교해 summary를 출력해야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 triage와 demo, load_json 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test-unit && make demo-dependency` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
