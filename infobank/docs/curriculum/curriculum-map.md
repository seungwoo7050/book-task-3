# 커리큘럼 맵

## 공통 단계 의미

- `00`: 문제 정의, 참고 기준, 최종 방향을 먼저 고정한다.
- `01~07`: capstone을 구성하는 핵심 개념을 작은 학습 단위로 분리한다.
- `08`: 실제로 보여 줄 수 있는 capstone 버전 스냅샷과 제출 자료를 정리한다.

## 1번 과제: `projects/01-mcp-recommendation-demo/`

| 단계 | 프로젝트 | 배우는 것 | 포트폴리오로 가져갈 것 |
|---|---|---|---|
| 00 | source-brief | MCP 추천 문제 공간, 참고 문헌, capstone 목표를 고정한다 | 문제 정의와 레퍼런스 스파인 작성법 |
| 01 | selection-rubric-and-eval-contract | 추천 품질 기준과 오프라인 평가 계약을 정한다 | 평가 기준표와 acceptance threshold 문서화 |
| 02 | registry-catalog-and-manifest-schema | registry catalog와 manifest schema를 계약으로 만든다 | schema-first 설계와 검증 가능한 데이터 계약 |
| 03 | differentiation-and-exposure-design | 한국어 추천 근거와 차별화 문구를 설계한다 | 사용자 설명 문구와 노출 전략 |
| 04 | selector-baseline-and-reranking | baseline selector와 reranker를 구현한다 | 추천 로직 비교와 실험 설계 |
| 05 | usage-logs-metrics-and-feedback-loop | 사용 로그, 피드백, 실험 메타데이터를 연결한다 | 운영 지표와 피드백 루프 설계 |
| 06 | release-compatibility-and-quality-gates | compatibility, quality gate, artifact export를 구현한다 | 배포 전 검증과 제출용 증빙 산출물 |
| 07 | operator-dashboard-and-experiment-console | 운영자 콘솔과 실험 대시보드를 완성한다 | 운영 화면과 실험 콘솔 IA |
| 08 | capstone-submission | `v0 -> v3` 버전 스냅샷으로 최종 데모를 관리한다 | 버전 스냅샷과 self-hosted 확장 전략 |

## 2번 과제: `projects/02-chat-qa-ops/`

| 단계 | 프로젝트 | 배우는 것 | 포트폴리오로 가져갈 것 |
|---|---|---|---|
| 00 | source-brief | 과제 해석, reference spine, baseline capstone 방향을 고정한다 | 문제 정의 문서와 학습 범위 선언 |
| 01 | quality-rubric-and-score-contract | 품질 축, 점수 계약, critical override 규칙을 정의한다 | score contract와 평가 언어 통일 |
| 02 | domain-fixtures-and-chat-harness | 상담 도메인 fixture와 replay harness를 만든다 | 재현 가능한 평가 입력셋 설계 |
| 03 | rule-and-guardrail-engine | 안전 규칙, PII, mandatory notice, escalation을 구현한다 | 규칙 기반 guardrail과 failure taxonomy |
| 04 | claim-and-evidence-pipeline | claim 추출과 근거 검증 파이프라인을 구현한다 | trace 중심 groundedness 설명 |
| 05 | judge-and-score-merge | judge 출력과 점수 합산 정책을 만든다 | 판단 로직과 점수 계약의 분리 |
| 06 | golden-set-and-regression | golden set, compare manifest, 회귀 검증 흐름을 만든다 | 개선 증빙과 regression proof |
| 07 | monitoring-dashboard-and-review-console | 운영 대시보드와 세션 리뷰 콘솔을 만든다 | 운영 UI와 리뷰 도구 설계 |
| 08 | capstone-submission | `v0 -> v3` 버전 스냅샷으로 제출/운영 데모를 정리한다 | stage 학습을 제품형 데모로 묶는 법 |
