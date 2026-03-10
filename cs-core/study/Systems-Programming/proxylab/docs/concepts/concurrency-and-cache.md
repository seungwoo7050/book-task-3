# concurrency와 cache를 함께 다뤄야 하는 이유

## 이 프로젝트의 세 마일스톤

`proxylab`은 보통 다음 순서로 이해하는 편이 좋습니다.

1. sequential forwarding
2. detached thread 기반 concurrent handling
3. in-memory cache

이 저장소의 구현은 세 단계 모두를 포함합니다.

## threading model

기본 루프는 다음처럼 단순합니다.

1. `accept`
2. connected fd를 heap에 저장
3. detached thread 생성
4. 곧바로 다음 `accept`

이 구조의 장점은 accept loop가 단순하고, concurrent test가 분명해진다는 점입니다.

## cache 설계

cache는 process-wide shared state입니다.
각 entry는 보통 다음 정보를 가집니다.

- request URI
- response byte copy
- response size
- LRU 연결을 위한 prev/next

정책은 다음 둘로 요약됩니다.

- `MAX_OBJECT_SIZE` 이하만 cache
- 총 크기가 `MAX_CACHE_SIZE`를 넘으면 tail부터 eviction

## locking discipline

이 저장소는 cache 전체에 하나의 mutex를 씁니다.
더 세밀한 locking도 가능하지만, 학습 목표는 다음이기 때문입니다.

- shared state를 안전하게 다루는 법
- LRU mutation이 깨지지 않게 하는 법
- cache hit path와 client I/O를 분리하는 법

실제로는 hit 시 객체를 lock 안에서 복사하고, client write는 unlock 뒤에 수행합니다.
그래야 네트워크 I/O 때문에 cache lock을 오래 잡지 않게 됩니다.

## 이 프로젝트가 보여 주는 것

프록시에서는 네트워크와 동시성이 분리된 문제가 아닙니다.
request 처리 흐름과 shared cache 정책이 항상 같이 움직입니다.
