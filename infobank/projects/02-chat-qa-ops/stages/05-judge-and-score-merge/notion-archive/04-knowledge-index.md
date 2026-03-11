> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Judge & Score Merge — 지식 인덱스

## 핵심 개념

| 개념 | 설명 | 관련 코드/파일 |
|------|------|---------------|
| 휴리스틱 judge | LLM 없이 규칙 기반으로 응답 품질을 채점하는 방식. failure 개수, 응답 길이, 키워드 포함 여부로 correctness/resolution/communication 점수를 산출한다. | `judge.py → judge_response()` |
| score merge | 5개 품질 축(correctness, resolution, communication, empathy, efficiency) 점수를 가중 평균으로 합산하는 과정. stage 01에서 정의한 WEIGHTS를 그대로 재사용한다. | `judge.py → merge_score()` |
| critical override | 합산 점수가 아무리 높아도, 특정 축 점수가 0이면 전체 점수를 0.0으로 덮어쓰는 규칙. stage 01 rubric에서 정의한 정책을 merge 단계에서 실행한다. | `rubric.py → merge_score()` |
| judge output schema | `{"correctness": float, "resolution": float, "communication": float}` — judge가 무엇이든(heuristic이든 LLM이든) 이 형태만 반환하면 merge에서 처리 가능하다. | `test_judge.py` |
| 가중치 축 | correctness(0.30), resolution(0.25), communication(0.20), empathy(0.15), efficiency(0.10) — merge 시 각 축에 곱해지는 비율 | `rubric.py → WEIGHTS` |

## 참고 흐름

```
stage 03 failure_types → judge_response() → per-axis scores
                                               ↓
stage 01 WEIGHTS ──────→ merge_score() ──→ total_score
                                               ↓
stage 01 GRADE_BANDS ──→ to_grade() ───→ "A"/"B"/"C"/"D"/"F"
```

## 다음 단계 연결

- **stage 06**: judge+merge가 생산한 score를 golden set에 대해 실행하고, baseline 대비 regression 여부를 판정한다.
- **capstone v1**: heuristic judge를 LLM judge로 교체하되, merge_score()와 to_grade()는 변경하지 않는다.
