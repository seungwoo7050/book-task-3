# Problem

## canonical problem statement

영속 계층 위에 도메인 이벤트를 붙여 side effect를 분리하고 테스트로 경계를 고정하는 것이 canonical problem이다.

## 성공 기준

- 도메인 이벤트와 리스너를 명시적으로 분리할 것
- 성공/실패 경로의 이벤트 발행 여부를 테스트할 것
- native SQLite 의존성을 포함한 재현 절차를 문서화할 것

## 제공 자료

- Express/NestJS starter code
- 이벤트 예제 코드
- 개념 문서
- 복구 가이드

## 이 문제를 푸는 공개 답안

- [Express 레인](../express/README.md)
- [NestJS 레인](../nestjs/README.md)
