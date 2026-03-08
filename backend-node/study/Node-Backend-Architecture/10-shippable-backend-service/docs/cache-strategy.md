# Cache Strategy

## 사용 범위

Redis 캐시는 public read 경로에만 적용한다.

- `GET /books` -> `books:list`
- `GET /books/:id` -> `books:detail:<id>`

## invalidation 규칙

- `POST /books`
- `PUT /books/:id`
- `DELETE /books/:id`

쓰기 요청이 성공하면 list cache와 대상 detail cache를 즉시 삭제한다.

## 의도한 단순화

- 캐시 prewarming은 하지 않는다.
- cache stampede 완화는 다루지 않는다.
- queue/worker로 캐시 무효화를 분산하지 않는다.

이 과제의 목적은 “읽기 경로 캐시 + 쓰기 후 invalidation”이라는 기본 패턴을
작고 설명 가능한 수준으로 보여 주는 것이다.
