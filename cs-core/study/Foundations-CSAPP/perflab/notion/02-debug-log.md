# 02. 디버그 기록

## 실제로 다시 확인한 포인트

### 1. set/tag 분해 오프셋 계산

bit shift 하나만 틀려도 hit/miss 통계가 전부 무너진다.
그래서 simulator는 oracle을 먼저 맞춘 뒤 넘어가는 편이 안전했다.

### 2. hit 시 LRU 갱신 누락

eviction만 생각하고 hit 경로 갱신을 빼먹으면, 나중에 victim 선택이 계속 어긋난다.

### 3. `64x64`에서 단순 `8x8` block 재사용

`32x32`에선 잘 되던 전략이 `64x64`에서는 conflict miss를 과하게 만들었다.
이 크기만 별도 전략이 필요한 이유가 여기서 드러났다.

### 4. miss threshold 해석

숫자만 맞추는 것이 아니라, 왜 그 miss가 나왔는지 설명할 수 있어야 했다.
