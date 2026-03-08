# Core Concepts

## 핵심 개념

- `players`, `items`, `inventory` 분리는 다대다 관계를 명시적으로 드러낸다.
- `PRIMARY KEY (player_id, item_id)`는 같은 아이템의 중복 행 생성을 막는다.
- join query는 정규화된 데이터를 읽기 쉬운 뷰로 복원하는 단계다.
- transaction은 “재고 갱신이 반만 되는 상태”를 막는 최소 단위다.

## Trade-offs

- 초반에는 정규화가 이해를 돕지만, 읽기 성능 최적화 단계에서는 비정규화가 필요할 수 있다.
- SQLite in-memory는 입문에는 좋지만 실제 운영 DB의 락/격리 수준과는 다르다.

## 실패하기 쉬운 지점

- FK를 빼면 join은 되지만 데이터 무결성은 깨질 수 있다.
- `quantity <= 0` 같은 제약을 SQL과 애플리케이션 양쪽에서 동시에 생각하지 않으면 빈틈이 생긴다.

