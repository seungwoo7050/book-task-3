# Core Concepts

## 핵심 개념

- 구매 흐름은 transaction, idempotency, optimistic locking, relay를 동시에 건드린다.
- capstone의 핵심은 새 알고리즘보다 “여러 운영 제약이 한 곳에서 만날 때의 구조”다.
- e2e 테스트는 unit test가 놓치는 통합 문제를 빠르게 드러낸다.

## Trade-offs

- 모든 요소를 한 프로젝트에 넣으면 학습 효과는 크지만 구조 이해가 느려질 수 있다.
- relay와 DB를 분리하지 않으면 단순하지만 장애 모델이 불분명해진다.

## 실패하기 쉬운 지점

- idempotency와 optimistic locking을 따로 이해해도 실제 구매 흐름에서 둘의 상호작용을 놓치기 쉽다.
- evidence 자산을 raw log로만 남기면 공개 저장소에서 읽기 어렵다.

