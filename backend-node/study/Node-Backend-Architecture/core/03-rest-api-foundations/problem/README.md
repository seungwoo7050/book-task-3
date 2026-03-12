# Problem

## canonical problem statement

동일한 Books CRUD를 Express와 NestJS로 각각 구현하면서 레이어 분리와 DI를 비교 학습하는 것이 canonical problem이다.

## 성공 기준

- 두 레인 모두 `GET/POST/PUT/DELETE /books` 계약을 구현할 것
- service가 HTTP 세부사항에 의존하지 않게 분리할 것
- 두 레인의 테스트와 실행 명령이 README에 명시될 것

## 제공 자료

- Express starter code
- NestJS starter code
- Makefile 기반 원본 실행 힌트
- 개념 문서와 비교 노트

## 이 문제를 푸는 공개 답안

- [Express 레인](../express/README.md)
- [NestJS 레인](../nestjs/README.md)
