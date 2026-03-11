> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Guardrail Engine — 지식 인덱스

## 핵심 개념

### Rule-based Guardrail

LLM의 판단에 의존하지 않고, **미리 정의된 규칙**으로 위반을 검출하는 방식이다.
장점은 deterministic하고 설명 가능하다는 것. 단점은 동의어나 문맥 변형에 약하다는 것.
이 stage에서는 장점이 목적에 부합하므로 rule-based를 선택했다.

### Failure Type Taxonomy

실패를 "나쁘다"로 뭉치지 않고, **어떤 종류로 나쁜지** 분류하는 체계다.
이 프로젝트의 taxonomy:
- **MISSING_MANDATORY_STEP**: 필수 절차(본인확인) 누락
- **UNSUPPORTED_CLAIM**: 보장할 수 없는 약속
- **PII_EXPOSURE**: 개인정보 노출
- **ESCALATION_MISS**: 전문 상담 이관 미안내

### 한국어 상담 시나리오의 Escalation 조건

한국어 상담에서는 "민원", "분쟁", "피해"와 같은 표현이 escalation 트리거가 된다.
이 표현이 등장했을 때 상담원이나 전문 부서 연결을 안내하지 않으면, 고객 불만이 확대될 수 있다.

## 참고 자료

### Mandatory Notice And Escalation Rules (capstone)

- **경로**: `08-capstone-submission/v0-initial-demo/python/backend/rules/mandatory_notices.yaml`
- **왜 읽었나**: v0에 반영한 한국어 안전 규칙을 stage pack으로 축소 재현하기 위해
- **배운 것**: mandatory notice와 escalation은 둘 다 compliance이지만 **실패 원인이 달라** 별도 분리가 필요
- **이후 영향**: stage 03에서 escalation miss를 전용 failure code로 유지
