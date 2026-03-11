# 루브릭 명세

## 점수 축

| Dimension | Meaning | Weight |
|---|---|---|
| Correctness | 답변 내용의 사실성 | 0.30 |
| Groundedness | 근거 문서 기반성 | 0.25 |
| Compliance | 정책/절차 준수 | 0.20 |
| Resolution | 문제 해결 도움 정도 | 0.15 |
| Communication | 표현 명확성, 어조 | 0.10 |

## 즉시 실패 조건

아래는 총점과 별도로 즉시 실패 처리한다.

- PII 노출
- 금지된 약속
- 치명적 정책 위반
- 근거 충돌

## 실패 분류 기준선

- `FORBIDDEN_PROMISE`
- `PII_EXPOSURE`
- `MISSING_MANDATORY_STEP`
- `UNSUPPORTED_CLAIM`
- `CONTRADICTED_BY_SOURCE`

## 등급 규칙

- `CRITICAL`: 즉시 실패
- `A`: 90+
- `B`: 75+
- `C`: 60+
- `D`: 40+
- `F`: 40 미만
