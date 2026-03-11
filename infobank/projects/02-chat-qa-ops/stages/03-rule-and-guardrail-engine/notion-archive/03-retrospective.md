> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Guardrail Engine — 회고

## 잘 된 것

### 실패 이유가 명확해졌다

`MISSING_MANDATORY_STEP`, `UNSUPPORTED_CLAIM`, `PII_EXPOSURE`, `ESCALATION_MISS` — 이름만 봐도 뭐가 잘못됐는지 안다.
human review에서 "이 답변은 왜 나쁜가?"에 즉시 답할 수 있게 되었다.

### golden regression에서 재현 가능한 failure taxonomy를 제공한다

v0 → v1 개선 실험에서 "MISSING_REQUIRED_EVIDENCE_DOC가 14에서 11로 줄었다"는 보고가 가능한 건,
failure type이 코드화되어 있기 때문이다. generic "compliance low"로는 이런 추적이 안 된다.

## 아쉬운 것

### rule coverage 확장은 수동 유지보수 비용이 든다

새로운 정책이 생길 때마다 `rules.json`에 키워드를 추가해야 한다.
동의어나 문맥 변형(예: "확실히 되나요?"는 과장 약속인가?)은 keyword matching으로 잡히지 않는다.

## 나중에 다시 볼 것

- 실제 상담 로그를 더 확보하면, synonym dictionary를 늘리거나 regex DSL을 도입할 수 있다.
- LLM-based compliance checker와 rule-based checker를 **병행**하는 하이브리드 접근도 고려할 수 있다.
