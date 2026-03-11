> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Domain Fixtures — 회고

## 잘 된 것

### fixture와 harness 경계가 분명해졌다

KB를 바꾸려면 `data/knowledge_base/` 아래 Markdown만 수정하면 된다.
replay 시나리오를 바꾸려면 `data/replay_sessions.json`만 수정하면 된다.
harness 로직을 바꿔도 fixture는 그대로다.
이 분리 덕에 "무엇이 바뀌었는지"를 git diff로 추적하기 쉽다.

### 사람이 읽을 수 있는 KB와 replay transcript를 유지했다

Markdown과 JSON이라는 포맷 선택이 의외로 큰 차이를 만들었다.
code review 때 "이 테스트 데이터가 맞나?"를 확인하려면, 파일을 열어서 한국어 문장을 직접 읽을 수 있어야 한다.
바이너리 형식이나 embedding 인덱스라면 이게 불가능하다.

## 아쉬운 것

### 실제 고객 대화처럼 다중 턴 상태를 반영하지 않는다

현재 replay session은 단일 질의 → 단일 검색이라는 구조다.
실제 상담에서는 "환불 가능해요?" → "네, 본인확인 필요해요" → "본인확인은 어떻게 해요?"처럼 대화가 이어진다.
이 stage에서는 multi-turn을 다루지 않았다.

## 나중에 다시 볼 것

- replay fixture를 YAML까지 확장하면 capstone의 richer metadata를 더 잘 반영할 수 있다.
- 실제로 capstone v0~v2에서는 `replay_sessions.yaml`을 사용하고 있어서, 이 stage의 JSON 포맷과 차이가 있다.
