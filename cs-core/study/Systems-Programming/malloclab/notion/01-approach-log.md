# Malloc Lab — 접근 기록

## 설계 공간 탐색: 어떤 allocator를 만들 것인가

### 첫 번째 선택 — 프리리스트 구조

교과서는 세 가지 단계를 보여준다:

1. **Implicit free list**: 모든 블록을 순회하며 free 블록을 찾는다. O(total blocks).
2. **Explicit free list**: free 블록만 이중 연결 리스트로 관리한다. O(free blocks).
3. **Segregated free list**: 크기 클래스별로 분리된 리스트. O(1)에 가까운 탐색.

나는 explicit free list를 선택했다. Implicit보다 현실적이면서, segregated까지 가면 코드 복잡도가 급격히 올라가 학습 목적과 맞지 않는다. 핵심 개념 — 블록 산술, 경계 태그, 리스트 조작, 병합 — 을 모두 포함하되 코드를 손으로 추적할 수 있는 수준이 목표였다.

### 두 번째 선택 — 블록 레이아웃

```
[ 8-byte header ][ payload (≥ 16 bytes) ][ 8-byte footer ]
```

- 최소 블록 = 32바이트 (header 8 + next/prev 포인터 16 + footer 8)
- 16바이트 정렬: 블록 크기를 항상 16의 배수로 유지
- 헤더/푸터 하위 4비트를 플래그에 사용 (bit 0 = allocated)

Free 블록에서 payload 영역 처음 16바이트를 next/prev 포인터로 재활용한다. 할당된 블록은 이 포인터가 필요 없으므로 payload가 온전하다.

### 세 번째 선택 — 병합 정책

**즉시 병합(eager coalescing)**: free 시점에 즉시 이웃을 확인하고 합친다. 지연 병합(deferred)이 throughput에서 유리할 수 있지만, eager가 힙 상태를 항상 정규 형태로 유지해 디버깅과 추론이 쉽다.

### 네 번째 선택 — 탐색 정책

**First-fit**: 리스트를 앞에서부터 순회하며 첫 번째 맞는 블록을 반환한다. Best-fit은 utilization이 나을 수 있지만 O(n) 전체 순회가 필수다. 하나의 리스트에서 first-fit이 구현 단순성과 성능의 합리적 타협이다.

---

## 힙 초기 레이아웃

`mm_init`의 설계:

```
offset 0:   [  패딩  ]     (8 bytes, 정렬용)
offset 8:   [ prologue header: size=16, alloc=1 ]
offset 16:  [ prologue footer: size=16, alloc=1 ]
offset 24:  [ epilogue header: size=0, alloc=1  ]
```

Prologue는 "절대 free되지 않는 경계 블록"으로, `previous_block()` 호출 시 힙 경계를 넘어가지 않게 보호한다. Epilogue는 `next_block()` 순회의 종단점이다.

초기화 직후 `extend_heap(4096)`으로 첫 free 블록을 확보한다.

---

## 핵심 연산의 구현 사고

### malloc

```
1. size == 0 → return NULL
2. adjusted = align(size + 16)  // overhead: header + footer
3. adjusted = max(adjusted, 32) // 최소 블록
4. find_fit(adjusted)로 free 리스트 탐색
5. 없으면 extend_heap(max(adjusted, 4096))
6. place_block: split 가능하면 나머지를 free 블록으로 분리
```

### free

```
1. ptr == NULL → return
2. header/footer를 free로 마킹
3. coalesce: 4-way 분기 (prev/next 각각 alloc/free)
```

### realloc

세 가지 경로:

1. **현재 블록이 충분히 큼**: shrink-split 후 그대로 반환. 이동 없음.
2. **다음 블록이 free이고 합치면 충분**: in-place growth. memcpy 없이 header/footer만 확장. 이 경로가 있고 없고가 realloc 성능에 결정적이다.
3. **어디서도 안 되면**: malloc → memcpy → free. 마지막 수단.

보존해야 할 payload 크기는 `min(old_size - overhead, new_size)`이다.

---

## 구현 순서

1. 블록 레이아웃 헬퍼 함수군 (`header_of`, `footer_of`, `next_block`, `previous_block`)
2. Free-list 조작 (`add_to_free_list`, `remove_from_free_list`)
3. `mm_init` + `extend_heap`
4. `mm_malloc` (find_fit + place_block)
5. `mm_free` + `coalesce`
6. `mm_realloc` (in-place growth path 포함)

이 순서로 하면 각 단계에서 트레이스 하나씩 통과시킬 수 있다 — basic.rep → coalesce.rep → realloc.rep → mixed.rep.
