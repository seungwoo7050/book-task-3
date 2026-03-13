# 03-rest-api-foundations structure plan

이 문서는 "CRUD를 만들었다"보다 "같은 CRUD를 Express와 NestJS가 어디서 다르게 감싸는가"가 먼저 읽혀야 한다. 서사의 중심은 `manual DI -> container DI -> 같은 계약 검증`이다.

## 읽기 구조

1. 왜 이 프로젝트가 `core`의 첫 비교 지점인지 짚는다.
2. Express에서 service/router/controller 경계를 세운 장면을 먼저 보여 준다.
3. NestJS에서 같은 문제를 decorator와 DI로 옮긴 장면을 잇는다.
4. 테스트가 두 레인을 어떻게 서로 다른 방식으로 고정하는지로 마무리한다.

## 반드시 남길 근거

- Express `BookService`
- Express `createBookRouter`
- Nest `BooksService`
- Nest `BooksController`
- Express `build && test`
- Nest `build && test && test:e2e`

## 리라이트 톤

- Express와 NestJS를 우열 비교하지 않는다.
- 같은 문제를 다른 표면으로 감싼다는 인상이 먼저 들게 쓴다.
