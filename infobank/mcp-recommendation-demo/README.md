# Study1 MCP Recommendation Optimization

Study1의 주제는 MCP 추천 최적화이며, 최종 capstone은 운영형 MCP 추천 시스템 데모다.

## Sequence

- 00-source-brief: MCP 추천 최적화 study1의 문제 공간, reference spine, capstone 목표를 한 페이지에서 정리한다.
- 01-selection-rubric-and-eval-contract: 추천 품질을 어떤 rubric과 offline eval contract로 판정할지 고정한다.
- 02-registry-catalog-and-manifest-schema: catalog seed와 manifest schema를 단일 계약으로 고정한다.
- 03-differentiation-and-exposure-design: 한국어 노출 문구, differentiation point, explanation template를 설계한다.
- 04-selector-baseline-and-reranking: baseline selector와 signal-based reranker를 단계적으로 구현한다.
- 05-usage-logs-metrics-and-feedback-loop: usage event, feedback record, experiment metadata를 DB와 API에 연결한다.
- 06-release-compatibility-and-quality-gates: semver/compatibility gate와 release gate를 deterministic rule로 구현한다.
- 07-operator-dashboard-and-experiment-console: catalog, experiment, release candidate를 한 화면에서 CRUD하는 운영 콘솔을 완성한다.
- 08-capstone-submission: v0, v1, v2를 나란히 두고 최종 데모 제출물을 관리한다.

## Capstone Versions

- 08-capstone-submission/v0-initial-demo: registry seed, manifest validation, baseline selector, 한국어 추천 근거, offline eval까지 동작하는 최초 runnable 데모.
- 08-capstone-submission/v1-ranking-hardening: v0를 복제한 뒤 reranker, usage logs, feedback loop, baseline/candidate compare, catalog/experiment CRUD를 추가한 버전.
- 08-capstone-submission/v2-submission-polish: v1를 복제한 뒤 compatibility gate, release gate, submission artifact export, dry-run pipeline, release candidate CRUD를 추가한 최종 버전.

## Validation Entry Points

- `08-capstone-submission/v0-initial-demo`: baseline selector + offline eval
- `08-capstone-submission/v1-ranking-hardening`: reranker + feedback loop + compare
- `08-capstone-submission/v2-submission-polish`: compatibility gate + release gate + artifact export

## Notes

- `legacy/`는 참조 전용이다.
- `notion/`은 로컬 전용 technical notebook이다.
- tracked 문서는 stable index 역할만 수행한다.
