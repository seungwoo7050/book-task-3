# 접근 로그

## 처음 고려한 선택지

1. 기존 `platform` 구조를 유지한 채 라우터만 `auth`와 `workspace`로 분리한다.
2. 서비스는 둘로 나누되 `workspace-service`가 필요할 때 `identity-service` DB를 읽게 둔다.
3. 서비스와 DB를 둘 다 나누고, 사용자 정보는 JWT claims로만 전달한다.

## 선택한 방향

세 번째 방식을 채택했다. `identity-service`와 `workspace-service`를 따로 두고, 사용자 식별자는 token claims만으로 전달하도록 고정했다.

## 그렇게 고른 이유

- 첫 번째 방식은 폴더만 나뉘고 운영 경계는 그대로라서 학습 가치가 낮다.
- 두 번째 방식은 당장은 편하지만 “서비스 분리”보다 “원격 DB 조회 허용”이 먼저 남는다.
- 세 번째 방식은 불편함이 분명하지만, 어떤 정보가 계약이고 어떤 정보가 내부 데이터인지 바로 드러난다.

## 의도적으로 단순화한 점

- claim에는 `sub`, `handle`, `email` 같은 최소 정보만 넣는다.
- profile 조회, 사용자 검색, 조직 디렉터리 같은 기능은 넣지 않는다.
- gateway를 두지 않고 internal API를 직접 호출한다.

## 이번 선택이 만들어낸 제약

- `workspace-service`는 “사용자 상세 정보가 더 필요하다”는 이유로 `identity-service` DB를 읽을 수 없다.
- `workspace-service` 테스트도 UUID 형식의 `sub` claim을 전제로 맞춰야 한다.
- 서비스 간 경계를 설명하는 비용이 늘어난다.

이 제약이 불편해 보여도, 다음 랩에서 이벤트와 gateway를 붙일 때 가장 중요한 기준점이 된다.
