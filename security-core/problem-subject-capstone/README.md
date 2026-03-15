# security-core 서버 캡스톤 문제지

`security-core` capstone은 crypto, auth, backend, dependency 판단을 하나의 remediation queue와 review artifact 흐름으로 다시 묶게 만드는 종합 과제입니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [90-capstone-collab-saas-security-review-python](90-capstone-collab-saas-security-review-python.md) | 시작 위치의 구현을 완성해 secure_baseline_bundle.json은 빈 remediation board를 만들어야 합니다, review_bundle.json은 crypto, auth, backend, dependency 결과를 모두 만들어야 합니다, demo_bundle.json은 artifact 7개와 markdown report를 생성해야 합니다를 한 흐름으로 설명하고 검증한다. | `make test-capstone && make demo-capstone` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
