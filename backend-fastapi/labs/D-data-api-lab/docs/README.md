# D-data-api-lab 설계 문서

이 폴더는 D-data-api-lab의 설계 설명을 모아 둔 곳입니다. 실행 순서보다 왜 이런 경계를 택했고 무엇을 설명해야 하는지를 먼저 정리합니다.

## 이 문서에서 먼저 볼 질문

- 엔터티 관계를 어디까지 API에 그대로 드러낼 것인가
- 소프트 삭제는 목록 조회에서 어떤 의미를 가지는가
- optimistic locking은 어떤 충돌을 막아 주는가

## 읽고 나면 설명할 수 있어야 하는 것

- service boundary와 repository 역할
- page-based pagination의 한계와 장점
- 충돌 감지와 버전 필드의 의미

## 역할이 다른 관련 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [현재 학습 노트](../notion/README.md)
