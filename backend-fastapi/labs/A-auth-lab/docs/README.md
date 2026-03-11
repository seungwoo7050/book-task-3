# A-auth-lab 설계 문서

이 폴더는 "어떻게 실행하는가"가 아니라 "왜 이렇게 풀었는가"를 설명하는 설계 문서입니다. 문제 정의는 `problem/`, 실행은 `fastapi/`, 작업 기록은 `notion/`이 맡고, 여기서는 인증 경계와 토큰 설계를 해설합니다.

## 이 문서에서 먼저 볼 질문

- access token과 refresh token을 왜 분리하는가
- 이메일 검증과 비밀번호 재설정을 같은 토큰 계열 문제로 어디까지 묶을 수 있는가
- cookie 인증에서 CSRF를 어디에서 차단해야 하는가

## 읽고 나면 설명할 수 있어야 하는 것

- 로컬 인증 흐름의 상태 전이와 실패 지점
- 계정 회복 흐름을 별도 토큰으로 나누는 이유
- Mailpit 같은 로컬 개발 도구를 쓰는 이유와 한계

## 역할이 다른 관련 문서

- canonical problem statement: [problem/README.md](../problem/README.md)
- 실행과 검증 entrypoint: [fastapi/README.md](../fastapi/README.md)
- 현재 학습 로그: [notion/README.md](../notion/README.md)
