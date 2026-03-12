# Problem

## canonical problem statement

Books API의 저장소를 in-memory에서 SQLite 기반 persistence로 바꾸면서 repository 경계를 설계하는 것이 canonical problem이다.

## 성공 기준

- 두 레인 모두 CRUD 계약을 유지한 채 저장 계층을 바꿀 것
- `better-sqlite3` 설치와 복구 절차를 문서화할 것
- unit/e2e 테스트로 저장 전략 교체 이후 동작을 검증할 것

## 제공 자료

- Express/NestJS starter code
- SQLite 기반 예제 코드
- 개념 문서
- 복구 가이드

## 이 문제를 푸는 공개 답안

- [Express 레인](../express/README.md)
- [NestJS 레인](../nestjs/README.md)
