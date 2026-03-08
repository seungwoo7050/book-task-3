# Rubric Spec

## Score Dimensions

| Dimension | Meaning | Weight |
|---|---|---|
| Correctness | 답변 내용의 사실성 | 0.30 |
| Groundedness | 근거 문서 기반성 | 0.25 |
| Compliance | 정책/절차 준수 | 0.20 |
| Resolution | 문제 해결 도움 정도 | 0.15 |
| Communication | 표현 명확성, 어조 | 0.10 |

## Hard Fail

아래는 총점과 별도로 즉시 실패 처리한다.

- PII exposure
- forbidden promise
- critical policy violation
- evidence contradiction

## Failure Taxonomy Baseline

- `FORBIDDEN_PROMISE`
- `PII_EXPOSURE`
- `MISSING_MANDATORY_STEP`
- `UNSUPPORTED_CLAIM`
- `CONTRADICTED_BY_SOURCE`

## Grade Rule

- `CRITICAL`: hard fail
- `A`: 90+
- `B`: 75+
- `C`: 60+
- `D`: 40+
- `F`: below 40
