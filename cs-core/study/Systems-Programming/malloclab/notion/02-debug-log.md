# Malloc Lab — 디버그 기록

## Bug 1: footer_of 계산 오프바이원

### 증상

`basic.rep` 첫 번째 free에서 coalesce가 epilogue를 삼켜 이후 할당이 전부 실패.

### 원인

`footer_of(block)`이 `block + size - WORD_SIZE`로 계산되었다. 올바른 값은 `block + size - DOUBLE_WORD`. 블록은 payload 시작 주소이고, footer는 블록 끝에서 header 크기(8)가 아니라 footer 자신의 크기(8)를 뺀 위치에 있다:

```
[header 8][payload...][footer 8]
 ^                     ^
 block - 8             block + size_from_header - 16
```

`block`은 header 바로 다음이므로 `block + block_size(header) - 2*WORD_SIZE`가 footer 주소다.

### 수정

```c
static void *footer_of(void *block)
{
    return (char *)block + block_size(header_of(block)) - DOUBLE_WORD;
}
```

### 교훈

블록 산술에서는 "포인터가 가리키는 위치가 header인가, payload인가"를 항상 먼저 확인한다. 이 프로젝트에서 `block` 포인터는 항상 payload 시작점이다.

---

## Bug 2: coalesce에서 병합된 블록의 footer 갱신 누락

### 증상

`coalesce.rep`에서 세 블록 연속 free 후 대형 할당 실패. free 리스트에 충분한 바이트가 있는데 단일 블록으로 인식되지 않음.

### 원인

prev + current + next를 모두 병합하는 4번째 분기에서:

```c
// 잘못된 버전
store_word(header_of(prev), pack(size, 0));
store_word(footer_of(block), pack(size, 0));  // block은 current
```

병합 후 footer는 `next` 블록의 끝에 있어야 하는데, `block`(중간 블록)의 footer에 쓰고 있었다.

### 수정

```c
store_word(header_of(prev), pack(size, 0));
store_word(footer_of(next), pack(size, 0));   // next의 footer = 병합 전체의 끝
```

물론 이 시점에서 `footer_of(next)` 계산에 필요한 `next`의 header는 아직 원래 값이므로, `footer_of`가 원래 next의 크기를 기반으로 올바른 위치를 가리킨다. 병합 후에는 `footer_of(prev)`가 같은 위치를 가리키게 된다.

### 교훈

4-way coalesce의 각 분기에서 "누구의 header를 쓰고, 누구의 footer를 쓰는가"를 그림으로 그리면 실수를 없앨 수 있다.

---

## Bug 3: realloc in-place growth 후 잔여 split 미등록

### 증상

`realloc.rep`에서 in-place growth 성공 후, 원래 next 블록 위치의 잔여 공간이 free 리스트에 누락. 이후 해당 영역이 할당 불가능한 "사라진 바이트"가 됨.

### 원인

next 블록을 흡수한 뒤 shrink-split은 했지만, split된 잔여 블록을 `add_to_free_list()`에 넣지 않았다.

### 수정

```c
if (remainder >= MIN_BLOCK_SIZE) {
    void *split = (char *)ptr + adjusted;
    store_word(header_of(ptr), pack(adjusted, 1));
    store_word(footer_of(ptr), pack(adjusted, 1));
    store_word(header_of(split), pack(remainder, 0));
    store_word(footer_of(split), pack(remainder, 0));
    add_to_free_list(split);  // ← 이 줄이 빠져 있었다
}
```

### 교훈

split이 발생할 때마다 "새로 생긴 free 블록은 반드시 리스트에 등록"이라는 불변식을 확인한다. place_block에서는 하고 있었는데 realloc 경로에서 놓친 것이다.

---

## Bug 4: extend_heap의 새 epilogue 위치

### 증상

힙을 두 번 확장한 뒤 할당하면 header가 엉뚱한 값을 읽어 segfault.

### 원인

`extend_heap`은 기존 epilogue를 새 free 블록의 header로 덮어쓰고, 새 epilogue를 끝에 배치해야 한다:

```c
// 기존 epilogue 위치 = sbrk 반환값 - WORD_SIZE
store_word(block - WORD_SIZE, pack(size, 0));    // 새 free header
store_word(block + size - DOUBLE_WORD, pack(size, 0)); // 새 free footer
store_word(block + size - WORD_SIZE, pack(0, 1));      // 새 epilogue
```

초기 버전에서 epilogue를 `block + size`에 배치하여 8바이트 밀렸다.

### 교훈

`mem_sbrk`가 반환하는 주소는 "이전 brk 위치"다. 이전 epilogue가 바로 그 직전(block - WORD_SIZE)에 있었다는 것을 기억하면 offset이 자연스럽게 나온다.

---

## 디버깅 기법 정리

### 패턴 검증

드라이버가 `fill_pattern` / `verify_pattern`으로 모든 payload를 바이트 단위 체크한다. 경계 오류가 있으면 "payload mismatch for id N at byte M"으로 정확한 위치를 알려준다.

### 겹침 감지

`verify_non_overlap`이 할당 때마다 모든 live 블록과 범위 교차 검사를 수행한다. O(n²)이지만 트레이스가 작아서 문제없고, 틀어진 블록 산술을 즉시 잡아낸다.

### 힙 상태 덤프

코드에 임시 `print_heap()` 함수를 추가하여 각 연산 후 전체 블록 체인을 출력하는 방식으로 디버깅했다. 블록마다 (주소, 크기, alloc, in_free_list) 네 컬럼을 찍으면 "어디서 일관성이 깨졌는가"가 한눈에 보인다.
