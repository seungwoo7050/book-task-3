# E-async-jobs-lab 문서 지도

이 문서는 요청 처리와 비동기 작업 실행을 분리할 때, 데이터 안정성과 재시도를 어떤 언어로 설명할지 정리하는 개념 지도입니다.

## 먼저 보면 좋은 질문

- 작업을 바로 실행하지 않고 outbox에 한 번 더 저장하는 이유는 무엇인가
- idempotency key는 중복 요청과 어떤 관계가 있는가
- retry 가능한 실패와 바로 종료해야 하는 실패는 어떻게 다른가

## 읽고 나면 설명할 수 있어야 하는 것

- outbox handoff boundary
- worker가 담당하는 책임
- 작업 상태 전이의 최소 모델

## 함께 보면 좋은 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [현재 학습 노트](../notion/README.md)
