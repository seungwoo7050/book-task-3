# B-federation-security-lab 문서 지도

이 문서는 외부 로그인과 2단계 인증이 세션 모델에 어떤 부담을 주는지 정리할 때 참고하는 개념 지도입니다.

## 먼저 보면 좋은 질문

- 외부 공급자 계정과 내부 사용자 계정을 어떻게 연결할 것인가
- 2FA를 로그인 흐름 어디에 끼워 넣을 것인가
- recovery code는 왜 평문으로 두면 안 되는가

## 읽고 나면 설명할 수 있어야 하는 것

- OIDC 진입과 내부 세션 발급의 차이
- 보안 강화 흐름의 단계 분리
- throttling과 audit log의 역할

## 함께 보면 좋은 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [현재 학습 노트](../notion/README.md)
