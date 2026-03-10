# cache simulator에서 꼭 이해해야 할 LRU

## 이 문서의 초점

Part A의 핵심은 trace 한 줄을 "캐시 상태 변화"로 정확히 번역하는 것입니다.
주소를 읽고 끝나는 것이 아니라, set 선택, tag 비교, hit/miss 판정, eviction까지 이어져야 합니다.

## 한 번의 접근에서 답해야 하는 질문

1. 이 주소는 어느 set으로 가는가
2. 그 set 안에서 어떤 tag가 있어야 hit인가
3. miss라면 비어 있는 line이 있는가
4. 없다면 어떤 line을 LRU victim으로 고를 것인가

이 네 질문이 곧 simulator의 뼈대입니다.

## LRU를 실수하기 쉬운 지점

- hit 때도 최근 사용 정보를 갱신해야 한다
- miss 후 빈 line에 넣을 때도 최근 사용 상태를 맞춰야 한다
- eviction 후보를 찾을 때 set 내부만 봐야 한다

Part A가 어렵게 느껴지는 이유는 구현량보다 상태 갱신 일관성 때문입니다.

## 이 저장소의 검증 방식

`study.trace`에 대해 세 가지 cache configuration에서 oracle 출력을 맞춥니다.

- `s=1 E=1 b=1` -> `hits=5 misses=10 evictions=8`
- `s=2 E=1 b=2` -> `hits=6 misses=9 evictions=7`
- `s=5 E=1 b=5` -> `hits=10 misses=5 evictions=0`

공식 trace를 재배포하지 않으면서도, LRU 구현 정합성을 설명 가능한 수준으로 고정한 셈입니다.
