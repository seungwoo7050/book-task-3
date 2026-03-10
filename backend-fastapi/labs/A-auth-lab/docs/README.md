# A-auth-lab 문서 지도

이 문서는 "인증 기능이 있다"를 넘어서, 왜 토큰 수명과 쿠키 방식을 이렇게 나눴는지 설명할 때 참고하는 개념 지도입니다.

## 먼저 보면 좋은 질문

- access token과 refresh token을 왜 분리하는가
- 이메일 검증과 비밀번호 재설정을 같은 토큰 문제로 볼 수 있는가
- cookie 인증에서 CSRF를 어디서 막아야 하는가

## 읽고 나면 설명할 수 있어야 하는 것

- 로컬 인증 흐름의 상태 전이
- 회복 흐름과 보안 경계
- Mailpit 같은 로컬 개발 도구를 왜 쓰는지

## 함께 보면 좋은 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [현재 학습 노트](../notion/README.md)
