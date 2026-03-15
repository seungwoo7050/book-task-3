# backend-spring 서버 개발 비필수 문제지

여기서 `비필수`는 Spring 학습 가치가 낮다는 뜻이 아니라, 서버 공통 필수보다 커머스형 웹 백엔드 문맥 의존성이 더 강하다는 뜻입니다.
이 트랙의 종합 과제는 [`../problem-subject-capstone/README.md`](../problem-subject-capstone/README.md)로 분리합니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [a-auth-lab-spring](a-auth-lab-spring.md) | 시작 위치의 구현을 완성해 회원가입, 로그인, refresh, logout, me 흐름이 현재 scaffold 안에서 동작한다와 refresh token rotation, 이메일 검증, 비밀번호 재설정, cookie + CSRF 경계를 설명할 수 있다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/A-auth-lab/spring && ./gradlew test` |
| [b-federation-security-lab-spring](b-federation-security-lab-spring.md) | 시작 위치의 구현을 완성해 Google OAuth2 authorize/callback 형태를 설명할 수 있는 federation flow가 존재한다, TOTP setup/verify와 recovery code 사고방식을 같은 랩에서 다룬다, audit 기록이 왜 필요한지 API와 문서 수준에서 설명할 수 있다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/B-federation-security-lab/spring && ./gradlew test` |
| [c-authorization-lab-spring](c-authorization-lab-spring.md) | 시작 위치의 구현을 완성해 organization 생성, invite 발급/수락, role 변경 흐름이 존재한다, 누가 어떤 조직/상점 리소스를 수정할 수 있는지 service logic 수준에서 설명 가능하다, 인증 랩의 문제와 authorization 랩의 문제가 문서와 코드에서 섞이지 않는다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/C-authorization-lab/spring && ./gradlew test` |
| [d-data-jpa-lab-spring](d-data-jpa-lab-spring.md) | 시작 위치의 구현을 완성해 Flyway와 JPA entity/repository/service 경계가 같이 보인다, pagination과 optimistic locking 같은 persistence 고민이 코드에 드러난다, Querydsl을 왜 지금은 얕게 두는지 설명할 수 있다를 한 흐름으로 설명하고 검증한다. | `cd /Users/woopinbell/work/book-task-3/backend-spring/labs/D-data-jpa-lab/spring && ./gradlew test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
