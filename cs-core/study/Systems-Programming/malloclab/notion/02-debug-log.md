# 02. 디버그 기록

## 실제로 다시 확인한 포인트

### 1. header/footer 위치 계산

오프셋 하나만 틀려도 footer 갱신이 잘못되고, 그 다음 coalescing이 연쇄적으로 무너진다.

### 2. split 후 free list 등록

남은 조각이 유효 free block이면 바로 free list에 넣어야 한다.
이걸 빼먹으면 allocator는 한동안 되는 것처럼 보여서 더 위험하다.

### 3. coalescing 후 링크 정리

병합된 옛 block이 free list 어딘가에 남아 있지 않은지 계속 확인해야 했다.

### 4. `realloc` copy 길이

새 크기가 아니라 "기존 payload와 새 payload 중 작은 쪽" 기준으로 복사해야 한다.
이 부분은 trace driver가 없으면 놓치기 쉽다.
