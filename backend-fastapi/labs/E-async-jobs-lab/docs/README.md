# E-async-jobs-lab 설계 문서

이 폴더는 E-async-jobs-lab의 설계 설명을 모아 둔 곳입니다. 실행 순서보다 왜 이런 경계를 택했고 무엇을 설명해야 하는지를 먼저 정리합니다.

## 이 문서에서 먼저 볼 질문

- 작업을 바로 실행하지 않고 outbox에 한 번 더 저장하는 이유는 무엇인가
- idempotency key는 중복 요청과 어떤 관계가 있는가
- retry 가능한 실패와 바로 종료해야 하는 실패는 어떻게 다른가

## 읽고 나면 설명할 수 있어야 하는 것

- outbox handoff boundary
- worker가 담당하는 책임
- 작업 상태 전이의 최소 모델

## 역할이 다른 관련 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [현재 학습 노트](../notion/README.md)
