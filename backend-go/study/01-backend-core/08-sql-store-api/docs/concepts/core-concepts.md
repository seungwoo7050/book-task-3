# Core Concepts

## 핵심 개념

- migration up/down은 스키마를 코드와 같이 추적하기 위한 최소 장치다.
- repository는 handler가 SQL 세부 사항을 직접 알지 않게 분리해 준다.
- optimistic update는 `version` 조건으로 충돌을 감지한다.
- transaction rollback은 실패한 재고 차감이 반만 남지 않게 한다.

## Trade-offs

- SQLite는 입문 학습에는 좋지만 실제 운영 환경의 concurrency 특성을 다 보여 주지는 않는다.
- repository 추상화는 테스트성을 높이지만 지나치면 작은 예제를 복잡하게 만들 수 있다.

## 실패하기 쉬운 지점

- `RowsAffected == 0`을 conflict로 처리하지 않으면 optimistic locking이 무의미해진다.
- migration down을 아예 테스트하지 않으면 나중에 롤백 감각이 약해진다.

