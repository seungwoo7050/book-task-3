> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Golden Set & Regression — 지식 인덱스

## 핵심 개념

| 개념 | 설명 | 관련 코드/파일 |
|------|------|---------------|
| golden set | 반드시 통과해야 하는 테스트 케이스 모음. 각 케이스는 id와 필수 근거 문서 ID를 명시한다. | `data/golden_cases.json` |
| golden case | golden set의 개별 항목. `required_evidence_doc_ids`로 해당 질문에 반드시 포함되어야 할 문서를 지정한다. | `golden_cases.json → cases[]` |
| evaluate_case | required doc IDs와 actual doc IDs를 비교하여 passed/reason_codes를 반환하는 함수 | `regression.py → evaluate_case()` |
| reason code | 실패 사유를 나타내는 문자열 상수. `MISSING_REQUIRED_EVIDENCE_DOC`는 필수 근거 문서 미포함을 의미한다. | `regression.py` |
| compare manifest | 두 버전(baseline, candidate)을 같은 dataset에 대해 비교하기 위한 설정 파일 | `data/compare_manifest.json` |
| baseline / candidate | 비교의 기준 버전과 대상 버전. 현재 v1.0(baseline) vs v1.1(candidate) | `compare_manifest.json` |

## 파이프라인 내 위치

```
stage 05 judge_response() ──→ per-case scores
                                    ↓
stage 06 evaluate_case() ──→ passed + reason_codes   ← golden_cases.json
                                    ↓
stage 06 load_manifest() ──→ baseline vs candidate    ← compare_manifest.json
                                    ↓
stage 07 dashboard ──→ version compare 시각화
```

## 다음 단계 연결

- **stage 07**: `GET /api/golden-run`이 golden set 실행 결과를 반환하고, `GET /api/compare`가 version compare 데이터를 반환한다.
- **capstone v1**: golden case를 20개 이상으로 확장하고, 점수 기반 regression threshold도 추가한다.
