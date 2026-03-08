# Core Concepts

## 핵심 개념

- cache-aside는 읽기 시 캐시를 먼저 보고, miss면 DB를 읽어 캐시에 채우는 패턴이다.
- 쓰기 후 invalidation을 빼먹으면 stale data가 남는다.
- structured logging은 trace id, path, method 같은 필드를 일관되게 남기는 습관이다.
- `/metrics`는 서비스 상태를 외부에서 긁어 갈 수 있는 최소 관측 지점이다.

## Trade-offs

- in-memory cache는 구조 학습에는 좋지만 프로세스 재시작과 다중 인스턴스에는 약하다.
- trace backend 없이 trace id만 남기면 상호 연동은 없지만 요청 상관관계는 잡을 수 있다.

## 실패하기 쉬운 지점

- update 이후 캐시 삭제를 빠뜨리면 테스트는 통과해도 운영에서는 오래된 값이 보일 수 있다.
- metrics를 텍스트로 직접 쓰면 간단하지만 라벨 모델링은 제한적이다.

