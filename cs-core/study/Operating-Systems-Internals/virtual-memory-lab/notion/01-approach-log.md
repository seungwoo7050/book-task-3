# 01 Approach Log

## 설계 선택

- trace를 줄 단위 텍스트 파일로 고정해 fixture diff가 쉬워지게 했다.
- `Frame`은 page 번호만 저장하지 않고 `dirty`, `loaded_at`, `last_used`, `referenced`까지 함께 보관하게 했다. policy별 로직을 한 구조 안에서 비교하기 위해서다.
- snapshot은 frame index보다 page 상태를 보기 쉽도록 page 번호 기준으로 정렬해 출력한다.
- summary는 `faults / hits / dirty_evictions`만 남겨, policy 비교에서 가장 필요한 숫자에 집중하게 했다.

## trace를 세 개만 둔 이유

- `belady.trace`: FIFO의 약점을 바로 보여 준다.
- `locality.trace`: LRU와 OPT가 왜 자주 함께 언급되는지 설명하기 좋다.
- `dirty.trace`: write-back cost를 의식하는 최소 예제로 충분하다.
