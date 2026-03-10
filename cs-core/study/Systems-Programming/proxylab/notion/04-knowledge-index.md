# 04. 지식 인덱스

## 핵심 개념과 다시 볼 이유

- absolute-form URI parsing: 프록시 입력을 origin server 요청으로 바꾸는 첫 관문이다.
- canonical proxy header rewrite: `Host`, `User-Agent`, `Connection`, `Proxy-Connection`을 어떻게 정규화하는지가 계약의 핵심이다.
- detached-thread model: thread lifetime과 연결 소유권을 먼저 정하지 않으면 동시성 버그가 금방 난다.
- mutex-protected LRU cache: 캐시 히트보다 먼저 일관성과 eviction 순서를 지켜야 한다.
- local origin harness 설계: 외부 서버에 기대지 않고 forwarding, cache, failure recovery를 반복 검증하기 위한 기반이다.

## 재현 중 막히면 먼저 확인할 것

- forwarding 설명: `../docs/concepts/http-forwarding.md`
- concurrency/cache 설명: `../docs/concepts/concurrency-and-cache.md`
- 현재 검증 순서: `../docs/references/verification.md`

## 이후 프로젝트와 연결되는 메모

- 네트워크 코드는 기능 시연보다 계약과 실패 복구를 먼저 설명할 때 훨씬 설득력 있다.
- 나중에 웹 서비스나 API 게이트웨이 문서를 쓸 때도 이 프로젝트의 재현 하네스 설계가 좋은 출발점이 된다.
