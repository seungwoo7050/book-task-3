# 02 Debug Log

## 실제로 다시 확인한 포인트

### 1. Clock hand 위치

Clock에서 hand를 eviction 뒤 어디로 넘길지 명확하지 않으면 replay가 비결정적으로 보일 수 있다. 이 프로젝트는 victim 다음 frame으로 hand를 넘기는 쪽으로 고정했다.

### 2. dirty bit 유지

dirty page hit에서 dirty bit를 유지하지 않으면 eviction 시점의 `dirty_evictions`가 틀린다. 읽기 hit와 쓰기 hit를 같은 코드 경로로 뭉치면 이 부분이 자주 빠진다.

### 3. OPT 미래 참조 계산

OPT는 단순해 보여도 “앞으로 다시 안 나오는 page를 우선 버린다”는 규칙을 정확히 구현해야 한다. future trace slicing을 잘못 잡으면 기준선 자체가 흔들린다.
