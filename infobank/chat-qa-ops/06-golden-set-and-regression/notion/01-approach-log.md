# Golden Set & Regression — 접근 기록

## golden_cases.json 설계

golden set의 최소 단위를 정해야 했다.
후보는 세 가지였다:

1. **질문 + 정답 텍스트**: 정답을 exact match로 비교
2. **질문 + 기대 점수 범위**: judge 점수가 특정 범위 안에 들어야 통과
3. **질문 + 필수 근거 문서 ID**: 검색 결과에 특정 문서가 포함되어야 통과

1번은 응답 문구가 조금만 바뀌어도 실패하므로 너무 취약하다.
2번은 judge 자체가 heuristic이라 점수 범위를 신뢰하기 어렵다.
3번을 택했다. 근거 문서 포함 여부는 retrieval 품질의 가장 직접적인 지표이고, 텍스트 변동에 강건하다.

결과 구조:

```json
{
  "cases": [
    {
      "id": "gs-001",
      "required_evidence_doc_ids": ["refund_policy.md"]
    }
  ]
}
```

## evaluate_case() 구현

핵심 로직은 한 줄이다:

```python
passed = any(doc_id in actual_doc_ids for doc_id in required_doc_ids)
```

`any()`를 쓴 이유: required_evidence_doc_ids 중 **하나라도** 실제 검색 결과에 포함되면 통과.
처음에는 `all()`로 했다가 바꿨다.
현실적으로 한 질문에 대해 여러 근거 문서가 있을 수 있고, 그중 하나만 찾아도 응답 품질은 유지된다.

## reason code 설계

실패 시 단순히 `False`만 반환하면 디버깅이 불가능하다.
어떤 이유로 실패했는지를 코드로 남겨야 한다.

현재 정의된 reason code:
- `MISSING_REQUIRED_EVIDENCE_DOC` — 필수 근거 문서가 검색 결과에 하나도 없음

이 패턴은 stage 03의 failure_types와 같은 방식이다.
문자열 상수로 정의하고, 리스트로 반환한다.

## load_manifest() 설계

compare manifest는 JSON 파일에서 로드한다.
복잡한 파싱이 필요 없으므로 `json.loads(path.read_text())`로 충분하다.

manifest가 반환하는 건 단순 dict다:
- `baseline`: 기준 버전 (예: "v1.0")
- `candidate`: 비교 대상 (예: "v1.1")
- `dataset`: 어떤 데이터셋으로 비교할지 (예: "golden-set")

이 정보는 stage 07 대시보드의 version compare 기능에서 사용된다.
