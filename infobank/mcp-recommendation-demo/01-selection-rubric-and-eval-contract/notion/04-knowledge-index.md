# Selection Rubric & Eval Contract — 지식 인덱스

## 핵심 개념

| 개념 | 설명 | 관련 파일 |
|------|------|-----------|
| selection rubric | 추천 품질을 측정하는 다축 평가 기준 (relevance, rank accuracy, coverage, diversity) | `contracts.ts` |
| offline eval contract | eval case를 자동 실행하고 rubric에 따라 점수를 매기는 계약 | `eval.ts`, `eval-service.ts` |
| acceptance threshold | 각 rubric 축의 최소 통과 기준. v0 baseline 기준으로 설정 | `eval-service.ts` |
| relevance | 추천된 도구가 요청과 관련 있는지 여부 (목록 포함 여부) | eval 평가 로직 |
| rank accuracy | 기대 1순위 도구가 실제 1순위인지 (strict 매칭) | eval 평가 로직 |
| coverage | eval case 전체에서 정답 도구를 얼마나 커버하는지 | eval 평가 로직 |
| diversity | 추천 결과가 카테고리별로 편중되지 않는지 | eval 평가 로직 |

## 구현 위치

| 기능 | capstone 버전 | 파일 |
|------|--------------|------|
| Zod eval schema | v0 | `shared/src/contracts.ts` |
| eval fixture | v0 | `shared/src/eval.ts` |
| eval service | v0 | `node/src/services/eval-service.ts` |
| eval route test | v0 | `node/tests/routes.integration.test.ts` |

## 다음 단계 연결

- **stage 02**: eval contract에 맞는 catalog와 manifest schema 확정
- **stage 04**: baseline selector가 이 rubric으로 몇 점인지 측정
