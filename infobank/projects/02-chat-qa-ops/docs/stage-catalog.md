# Chat QA Ops Stage Catalog

| Stage | 핵심 질문 | 대표 답 위치 | capstone 연결 |
| --- | --- | --- | --- |
| `00-source-brief` | 무엇을 만들고 어떤 경로로 읽게 할 것인가 | `stages/00-source-brief` | `capstone/v0-initial-demo` 기준점 |
| `01-quality-rubric-and-score-contract` | 상담 품질을 어떤 score contract로 계산할까 | `stages/01-quality-rubric-and-score-contract` | `v0~v2` scoring vocabulary |
| `02-domain-fixtures-and-chat-harness` | replay 입력을 어떻게 고정할까 | `stages/02-domain-fixtures-and-chat-harness` | `v0` replay harness |
| `03-rule-and-guardrail-engine` | 어떤 failure를 반드시 잡아야 할까 | `stages/03-rule-and-guardrail-engine` | `v0` guardrail rules |
| `04-claim-and-evidence-pipeline` | 답변과 근거를 어떻게 trace로 남길까 | `stages/04-claim-and-evidence-pipeline` | `v1` evidence verifier |
| `05-judge-and-score-merge` | judge 판단과 score merge를 어떻게 나눌까 | `stages/05-judge-and-score-merge` | `v1` judge pipeline |
| `06-golden-set-and-regression` | 개선을 어떤 manifest와 assertion으로 증명할까 | `stages/06-golden-set-and-regression` | `v1~v2` compare proof |
| `07-monitoring-dashboard-and-review-console` | 운영 콘솔은 trace를 어떻게 보여줘야 할까 | `stages/07-monitoring-dashboard-and-review-console` | `v1~v2` dashboard |
