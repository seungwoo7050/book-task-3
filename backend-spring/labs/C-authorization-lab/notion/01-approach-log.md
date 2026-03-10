# Approach Log — 인가 문제를 가장 작은 형태로 분리하기

## 선택지를 놓고 고민한 지점들

이 랩의 설계에서 가장 큰 갈림길은 "Spring Security의 method annotation을 얼마나 쓸 것인가"였다.

첫 번째 선택지는 `@PreAuthorize`를 바로 적용하는 것이었다. Spring Security 답고 실무적이지만, 첫 scaffold에서는 annotation 뒤에 숨은 **rule 자체가 보이지 않을 수 있다**. 학습자가 "이 annotation이 왜 여기 있지?"를 이해하려면, 먼저 rule이 어떤 모양인지를 알아야 한다.

두 번째는 service logic 중심으로 접근하는 것이었다. 단순하지만, annotation 기반 정책으로 확장할 여지를 명확히 남길 수 있다. "지금은 if문으로 권한을 체크하지만, 나중에 이걸 `@PreAuthorize`로 바꿀 수 있다"는 학습 경로가 분명해진다.

세 번째는 membership를 DB에 바로 넣는 것이었다. 현실적이지만, JPA 매핑과 마이그레이션까지 한꺼번에 다루면 초기 반복 속도가 느려진다. D-data-jpa-lab과 범위가 겹친다.

## 최종 선택: service logic 중심

결국 **service logic에서 authorization rule을 직접 구현하고, persistence는 인메모리로 유지**하는 방향을 택했다.

패키지 구조는 `authorization` 도메인 아래 `api`와 `application`으로 잡았다. `AuthorizationDemoService`에서 조직 생성 시 OWNER 역할을 자동 부여하고, invite 시 PENDING 상태를 거치며, accept 시 실제 역할로 전환하는 흐름이 **service logic으로 명시적**으로 드러난다.

이 선택이 맞다고 판단한 이유: authorization 문제를 가장 작은 형태로 분리해야, 이후 `@PreAuthorize`로 전환할 때 "무엇을 annotation으로 옮기는 건지"가 선명하다.

## 의식적으로 폐기한 아이디어들

**full auth integration**은 폐기했다. 인증과 인가를 같은 코드에서 다루면 실패 원인이 섞인다.
**policy engine(OPA 등) 도입**도 폐기했다. 이 랩의 범위를 넘는다.

## 이 결정을 뒷받침하는 근거

- `AuthorizationController.java` — organization 생성, invite, accept, role change가 REST 엔드포인트로 깔끔하게 분리
- `AuthorizationDemoService.java` — OWNER/PENDING/STAFF/MANAGER 역할 전환 로직이 순수 자바로 드러남
- `AuthorizationApiTest.java` — 전체 invite → accept → role change 흐름을 MockMvc로 증명
- `make test` — 테스트 통과 확인

