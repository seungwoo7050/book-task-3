# D-data-api-lab 문서 지도

이 문서는 CRUD 예제를 데이터 경계와 동시성 문제까지 확장해서 설명하려 할 때 참고하는 개념 지도입니다.

## 먼저 보면 좋은 질문

- 엔터티 관계를 어디까지 API에 그대로 드러낼 것인가
- 소프트 삭제는 목록 조회에서 어떤 의미를 가지는가
- optimistic locking은 어떤 충돌을 막아 주는가

## 읽고 나면 설명할 수 있어야 하는 것

- service boundary와 repository 역할
- page-based pagination의 한계와 장점
- 충돌 감지와 버전 필드의 의미

## 함께 보면 좋은 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [현재 학습 노트](../notion/README.md)
