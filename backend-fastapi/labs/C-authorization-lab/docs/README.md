# C-authorization-lab 설계 문서

이 폴더는 C-authorization-lab의 설계 설명을 모아 둔 곳입니다. 실행 순서보다 왜 이런 경계를 택했고 무엇을 설명해야 하는지를 먼저 정리합니다.

## 이 문서에서 먼저 볼 질문

- 역할과 소유권은 무엇이 다른가
- 초대 흐름에서 누가 상태를 바꿀 수 있는가
- 인가 규칙을 테스트하기 좋은 경계는 어디인가

## 읽고 나면 설명할 수 있어야 하는 것

- 워크스페이스 역할 표
- invitation lifecycle
- 리소스 접근 제어를 서비스 계층에서 다루는 이유

## 역할이 다른 관련 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [현재 학습 노트](../notion/README.md)
