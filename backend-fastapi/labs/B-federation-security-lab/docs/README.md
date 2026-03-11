# B-federation-security-lab 설계 문서

이 폴더는 B-federation-security-lab의 설계 설명을 모아 둔 곳입니다. 실행 순서보다 왜 이런 경계를 택했고 무엇을 설명해야 하는지를 먼저 정리합니다.

## 이 문서에서 먼저 볼 질문

- 외부 공급자 계정과 내부 사용자 계정을 어떻게 연결할 것인가
- 2FA를 로그인 흐름 어디에 끼워 넣을 것인가
- recovery code는 왜 평문으로 두면 안 되는가

## 읽고 나면 설명할 수 있어야 하는 것

- OIDC 진입과 내부 세션 발급의 차이
- 보안 강화 흐름의 단계 분리
- throttling과 audit log의 역할

## 역할이 다른 관련 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [현재 학습 노트](../notion/README.md)
