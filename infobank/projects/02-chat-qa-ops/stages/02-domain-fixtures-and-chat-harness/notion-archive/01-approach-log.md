> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Domain Fixtures — 접근 방식: 파일 분리와 단순 검색의 이유

## 핵심 결정

### 1. fixture를 코드 안에 하드코딩하지 않고 파일로 분리

golden set과 replay는 **사람이 diff로 검토할 수 있어야** 회귀 원인 분석이 쉽다.
JSON에 "환불은 몇일 걸려요?"라고 쓰여 있으면, 누구든 "이 입력이 맞나?"를 확인할 수 있다.
코드 안에 하드코딩하면 테스트를 실행해야만 입력을 볼 수 있다.

Knowledge base는 Markdown으로 분리했다. 이유는 두 가지:
- Markdown이면 사람이 직접 읽을 수 있다.
- 파일 이름(`refund_policy.md`, `identity_verification.md`)이 **문서 식별자** 역할도 한다.

Replay 세션은 JSON으로 분리했다. 각 세션에 `user_message`와 `expected_doc`을 명시해서, 테스트가 "이 질문에는 이 문서가 나와야 한다"를 검증할 수 있게 했다.

### 2. deterministic harness에 단순 keyword matching 사용

"Chroma나 FAISS를 바로 붙이면 안 되나?"라는 질문이 당연히 나온다.
하지만 이 stage의 목표는 search quality가 아니라 **재현 가능한 계약**이다.

vector DB를 쓰면 embedding model 버전, 인덱스 상태, 랜덤 시드 등 외부 의존성이 생긴다.
같은 입력에 다른 결과가 나올 수 있다.
반면 keyword matching은 **항상 같은 결과**를 보장한다.

실제 capstone(v0~v2)에서는 Chroma를 사용하지만, 이 stage pack에서는 의도적으로 단순하게 유지했다.

## 선택하지 않은 방향

- **stage pack에서 바로 Chroma나 live provider를 요구하는 방식**: 외부 의존성이 재현성을 해친다.
- **replay transcript를 테스트 파일에만 넣는 방식**: golden set과 dashboard에서 같은 데이터를 공유하려면 파일 분리가 필수다.

## 이 선택이 후속 stage에 미친 영향

- v0의 replay harness와 seeded KB는 이 stage의 설계를 확장한 것이다.
- v1/v2의 golden replay도 입력 fixture 분리가 핵심 원칙이다.
- stage 06에서 golden cases를 별도 JSON으로 관리하는 패턴은 여기서 시작됐다.
