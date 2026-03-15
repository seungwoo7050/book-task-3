# F-cache-concurrency-lab series map

이 시리즈는 `F-cache-concurrency-lab`을 "Redis 전 단계"라고만 보지 않고, 실제로 현재 코드가 어떤 종류의 idempotency와 cache inconsistency를 만드는지까지 같이 읽는다. 특히 이 lab은 inventory reservation을 보호하려고 하지만, 조회 캐시는 쓰기 뒤에 무효화되지 않고 idempotency key도 request fingerprint와 연결되지 않는다.

## 읽는 순서

1. [10-development-timeline.md](10-development-timeline.md)
   reservation path, 전역 `synchronized`, stale cache, idempotency key 재사용 결과를 순서대로 따라간다.

## 이 시리즈가 답하는 질문

- 현재 cacheable read path는 무엇을 캐시하고 무엇을 깨뜨리는가
- 지금의 idempotency는 "같은 요청 재실행"을 다루는가, 아니면 "같은 키 재사용"만 다루는가
- distributed lock 이전 단계라는 설명만으로는 가려지는 현재 한계가 무엇인가
