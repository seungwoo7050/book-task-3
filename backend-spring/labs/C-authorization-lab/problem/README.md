# C-authorization-lab 문제 정의

인증 문제와 분리된 authorization 랩을 만들어 role, membership, ownership 규칙을 명시적으로 다룬다.

## 성공 기준

- organization 생성, invite 발급/수락, role 변경 흐름이 존재한다.
- 누가 어떤 조직/상점 리소스를 수정할 수 있는지 service logic 수준에서 설명 가능하다.
- 인증 랩의 문제와 authorization 랩의 문제가 문서와 코드에서 섞이지 않는다.

## 이번 단계에서 다루지 않는 것

- PostgreSQL 기반 membership persistence
- Spring method security 재구성
- 외부 policy engine

이 디렉터리는 구현 답안이 아니라 canonical problem statement와 성공 기준을 위한 공간이다.
