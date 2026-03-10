# Knowledge Index — 이 랩에서 가져갈 개념들

## 재사용 가능한 핵심 개념

### Membership Lifecycle

조직 소속은 **즉시 부여보다 invite 상태를 거치는 것이 안전하다**. 이 랩의 `AuthorizationDemoService`에서 `invite()` 호출 시 멤버 상태가 `PENDING`으로 설정되고, `accept()` 호출 시 실제 역할(STAFF, MANAGER 등)로 전환된다. 이 패턴의 장점은 초대 취소가 가능하고, 감사 추적이 명확하며, 의도하지 않은 권한 부여를 방지할 수 있다는 것이다. capstone에서 상점 멤버십 관리에 그대로 적용된다.

### Ownership Check

같은 role이라도 **생성자나 소유자에게만 허용되는 규칙**을 뜻한다. 이 랩에서는 조직 생성 시 `OWNER` 역할을 자동 부여하고, OWNER만 다른 멤버의 역할을 변경할 수 있는 구조를 암시한다. 실제 서비스에서 "자기 게시물만 삭제 가능", "자기 상점만 설정 변경 가능" 같은 규칙이 모두 ownership check의 변형이다.

### Declarative vs Imperative Authorization

annotation 중심 정책(`@PreAuthorize("hasRole('OWNER')")`)과 **service logic 중심 정책**(`if (!isOwner(user)) throw ...`)의 차이다. 이 랩은 의도적으로 imperative 방식을 택해서 rule의 형태를 먼저 드러냈다. declarative 방식은 코드가 깔끔해지지만, rule이 annotation 뒤에 숨는다. 둘 다 장단점이 있으며, 실무에서는 복합적으로 사용한다.

## 용어 정리

### RBAC (Role-Based Access Control)

역할 이름으로 **권한 묶음을 표현하는 방식**이다. "OWNER는 모든 것을 할 수 있고, MANAGER는 멤버를 관리할 수 있고, STAFF는 읽기만 가능" 같은 구조. 이 랩에서 `Organization.members()`가 `Map<String, String>` (email → role)인 것이 RBAC 모델의 최소 표현이다.

### Method Security

Spring에서 **메서드 호출 수준으로 권한 규칙을 적용하는 방식**이다. `@EnableMethodSecurity`를 활성화하고, 개별 메서드에 `@PreAuthorize`, `@PostAuthorize`, `@Secured` 같은 annotation을 붙인다. 이 랩에서는 아직 적용하지 않았지만, 다음 단계에서 service logic의 권한 체크를 annotation으로 옮기는 것이 목표다.

## 참고 자료

- **C-authorization-lab docs README** (`docs/README.md`): current scope와 next improvement를 맞추기 위해 작성했다. service logic 중심 scaffold라는 점이 핵심이며, declarative security 부재를 회고와 디버그 로그에서 분명히 적는 데 반영했다.
- **Spring Security Method Security Reference**: `@PreAuthorize` 표현식 문법과 SpEL 기반 권한 체크 방식을 참고했다. 이 랩에서 바로 적용하지는 않았지만, 다음 단계의 전환 방향을 잡는 데 사용했다.

