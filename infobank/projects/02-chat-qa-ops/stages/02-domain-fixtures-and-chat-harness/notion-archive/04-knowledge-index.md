> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Domain Fixtures — 지식 인덱스

## 핵심 개념

### Seeded KB 설계

"Seeded KB"란 테스트와 회귀 검증을 위해 **미리 준비해둔 지식 베이스**다.
실제 운영 환경에서는 KB가 지속적으로 업데이트되지만, 품질 평가를 재현하려면 **고정된 KB**가 필요하다.
이 stage에서는 세 개의 Markdown 파일로 seeded KB를 구성했다:
- `refund_policy.md` — 환불 정책
- `identity_verification.md` — 본인확인 절차
- `cancellation_policy.md` — 해지 정책

### Deterministic Replay Harness

replay harness는 "같은 입력이면 같은 출력"을 보장하는 실행 환경이다.
외부 API 호출이나 랜덤 요소가 없으므로, 어떤 시점에 돌려도 결과가 동일하다.
이것이 회귀 테스트의 전제 조건이다.

### Expected Evidence Document 확인 방식

replay session에는 `expected_doc` 필드가 있다.
이건 "이 질문에는 최소한 이 문서가 검색되어야 한다"는 최소 계약이다.
top-1이 기대 문서와 일치하는지 검증하는 방식으로 테스트를 구성했다.

## 참고 자료

### Replay Harness (capstone)

- **경로**: `08-capstone-submission/v0-initial-demo/python/backend/src/evaluator/replay_harness.py`
- **왜 읽었나**: capstone의 재생 경로를 축소 구현할 때 어떤 계약이 핵심인지 확인하기 위해
- **배운 것**: fixture 구조가 안정적이어야 regression과 dashboard 수치가 같은 입력을 공유할 수 있다
- **이후 영향**: stage 02는 KB와 replay JSON을 별도 파일로 분리
