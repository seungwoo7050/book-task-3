# security-core 서버 캡스톤 답안지

이 문서는 security-core capstone을 실제 source와 테스트만으로 해설하는 답안지다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [90-capstone-collab-saas-security-review-python](90-capstone-collab-saas-security-review-python_answer.md) | 시작 위치의 구현을 완성해 secure_baseline_bundle.json은 빈 remediation board를 만들어야 합니다, review_bundle.json은 crypto, auth, backend, dependency 결과를 모두 만들어야 합니다, demo_bundle.json은 artifact 7개와 markdown report를 생성해야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 _finding와 evaluate_scenario, scenario_control_ids 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test-capstone && make demo-capstone` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
