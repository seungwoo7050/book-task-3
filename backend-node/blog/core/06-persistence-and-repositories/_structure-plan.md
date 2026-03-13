# 06-persistence-and-repositories structure plan

이 문서는 새 기능보다 "저장 전략만 바꾸고 API 계약은 유지했다"는 흐름이 먼저 읽혀야 한다. 서사의 축은 `SQLite repository -> ORM repository -> 계약 유지 검증`으로 잡는다.

## 읽기 구조

1. Express에서 DB 초기화와 repository를 먼저 세운 이유를 잡는다.
2. NestJS가 같은 문제를 `Repository<Book>`로 어떻게 감싸는지 잇는다.
3. unit/e2e 검증이 왜 persistence swap의 핵심 증거가 되는지로 마무리한다.

## 반드시 남길 근거

- `createDatabase`
- Express `BookRepository`
- Nest `BooksService`
- Express repository unit test
- Nest database e2e
- 두 레인의 `build && test && test:e2e`

## 리라이트 톤

- SQL 설명문으로 흐르지 않는다.
- "저장 방식이 바뀌어도 바깥 계약은 어떻게 유지됐는가"가 먼저 보이게 쓴다.
