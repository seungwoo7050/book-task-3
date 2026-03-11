> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Golden Set & Regression — 디버그 기록

## any() vs all() 전환 문제

### 상황

처음 evaluate_case()를 `all()`로 구현했다:

```python
passed = all(doc_id in actual_doc_ids for doc_id in required_doc_ids)
```

golden_cases.json에 `required_evidence_doc_ids`가 하나인 케이스만 넣었을 때는 문제가 없었다.
하지만 향후 문서 ID를 여러 개 넣는 케이스를 고려하면, "하나만 맞아도 통과"가 맞는지 "전부 맞아야 통과"가 맞는지 결정해야 했다.

### 결론

`any()`로 변경했다.
이유: required_evidence_doc_ids는 "이 중 하나라도 관련 있으면 해당 주제에 대한 근거가 존재하는 것"이라는 의미로 사용한다.
만약 "이 문서들 전부 필요"라는 케이스가 생기면, 그건 별도의 golden case로 분리하는 게 낫다.

## reason code 누락 디버그

### 상황

초기 구현에서 `evaluate_case()`가 `{'passed': False}`만 반환했다.
테스트는 통과했지만, stage 07에서 실패 사유를 표시하려고 하니 reason 정보가 없었다.

### 해결

반환값에 `reason_codes` 리스트를 추가했다:

```python
return {
    'passed': passed,
    'reason_codes': [] if passed else ['MISSING_REQUIRED_EVIDENCE_DOC']
}
```

이 패턴은 stage 03의 failure_types와 일관되게 맞춘 것이다.
리스트를 쓰는 이유는, 나중에 여러 실패 사유가 동시에 발생할 수 있기 때문이다.
