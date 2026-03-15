# backend-spring 서버 개발 비필수 답안지

이 문서는 Spring 트랙의 elective 랩 네 개를 실제 `spring` 소스 기준으로 다시 정리한 답안지다. 공통점은 모두 커머스형 웹 백엔드 문맥이 강하다는 점이고, 차이는 인증, 인증 강화, 권한 모델, JPA 영속 계층을 각각 별도 설계 문제로 분리해 보여 준다는 데 있다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [a-auth-lab-spring](a-auth-lab-spring_answer.md) | 시작 위치의 구현을 완성해 회원가입, 로그인, refresh, logout, me 흐름이 현재 scaffold 안에서 동작한다와 refresh token rotation, 이메일 검증, 비밀번호 재설정, cookie + CSRF 경계를 설명할 수 있다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/A-auth-lab/spring && ./gradlew test` |
| [b-federation-security-lab-spring](b-federation-security-lab-spring_answer.md) | 시작 위치의 구현을 완성해 Google OAuth2 authorize/callback 형태를 설명할 수 있는 federation flow가 존재한다, TOTP setup/verify와 recovery code 사고방식을 같은 랩에서 다룬다, audit 기록이 왜 필요한지 API와 문서 수준에서 설명할 수 있다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/B-federation-security-lab/spring && ./gradlew test` |
| [c-authorization-lab-spring](c-authorization-lab-spring_answer.md) | 시작 위치의 구현을 완성해 organization 생성, invite 발급/수락, role 변경 흐름이 존재한다, 누가 어떤 조직/상점 리소스를 수정할 수 있는지 service logic 수준에서 설명 가능하다, 인증 랩의 문제와 authorization 랩의 문제가 문서와 코드에서 섞이지 않는다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring && ./gradlew test` |
| [d-data-jpa-lab-spring](d-data-jpa-lab-spring_answer.md) | 시작 위치의 구현을 완성해 Flyway와 JPA entity/repository/service 경계가 같이 보인다, pagination과 optimistic locking 같은 persistence 고민이 코드에 드러난다, Querydsl을 왜 지금은 얕게 두는지 설명할 수 있다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring && ./gradlew test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
