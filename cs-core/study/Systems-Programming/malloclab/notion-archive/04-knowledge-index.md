# Malloc Lab — 지식 인덱스

## 1. 블록 레이아웃과 경계 태그

| 항목 | 설명 |
|---|---|
| Header | 8바이트. 상위 비트 = 블록 크기, 하위 bit 0 = allocated |
| Footer | Header의 복제. `previous_block()`이 상수 시간에 작동하려면 필수 |
| Payload | 사용자 데이터. 할당 시 반환되는 포인터가 여기를 가리킴 |
| 최소 블록 | 32바이트 = header(8) + next/prev(16) + footer(8) |
| 정렬 | 16바이트. 블록 크기 자체를 16의 배수로 유지 |

경계 태그(boundary tag)의 핵심 가치: 임의 블록에서 이전 블록의 크기를 O(1)에 알 수 있다. 이것 없이는 backward coalescing이 불가능하다.

---

## 2. Free List 구조

| 연산 | 시간 | 설명 |
|---|---|---|
| `add_to_free_list` | O(1) | LIFO — 헤드 삽입 |
| `remove_from_free_list` | O(1) | 이중 연결 리스트 — prev/next 직접 접근 |
| `find_fit` | O(free blocks) | First-fit 순회 |

Free 블록의 payload 공간을 포인터 저장에 재활용한다:

```
offset 0 (from payload start): next_free (8 bytes)
offset 8:                      prev_free (8 bytes)
```

이 포인터들은 할당되면 payload 데이터로 덮어쓰이므로, free 블록에서만 유효하다.

---

## 3. 힙 구조

```
[padding 8] [prologue hdr 8] [prologue ftr 8] [blocks...] [epilogue hdr 8]
```

- **Prologue**: 크기 16, allocated. `previous_block()`의 경계 가드
- **Epilogue**: 크기 0, allocated. `next_block()` 순회의 종단점
- **extend_heap**: 기존 epilogue를 새 free 블록의 header로 덮어쓰고, 끝에 새 epilogue 배치

---

## 4. Coalescing 4-way 분기

| prev | next | 동작 |
|---|---|---|
| alloc | alloc | current만 free. 리스트 삽입 |
| alloc | free | current + next 병합. next 제거 후 병합 블록 삽입 |
| free | alloc | prev + current 병합. prev 제거 후 병합 블록 삽입 |
| free | free | prev + current + next 3-way 병합. prev, next 제거 후 삽입 |

핵심 규칙:
- 병합 대상 이웃을 **먼저 free list에서 제거**
- 크기를 합산하여 header/footer 갱신
- 결과 블록을 **free list에 삽입**

---

## 5. Place & Split

```
if (remainder >= MIN_BLOCK_SIZE) {
    // split: block에 요청 크기, 나머지를 새 free 블록
} else {
    // 내부 단편화 수용: 전체 블록 할당
}
```

MIN_BLOCK_SIZE(32바이트) 미만의 잔여는 유효한 free 블록을 구성할 수 없으므로 그대로 둔다.

---

## 6. Realloc 전략

| 우선순위 | 조건 | 동작 | 비용 |
|---|---|---|---|
| 1 | `ptr == NULL` | `malloc(size)` | 새 할당 |
| 2 | `size == 0` | `free(ptr)`, return NULL | 해제 |
| 3 | 현재 블록 ≥ 요청 | shrink-split 가능하면 분할 | 이동 없음 |
| 4 | next free + current ≥ 요청 | in-place 성장 | 이동 없음, O(1) |
| 5 | 이상 | malloc → memcpy → free | 전체 복사 |

In-place growth(#4)의 조건: `!is_allocated(header_of(next)) && current_size + next_size >= adjusted`

---

## 7. memlib 힙 시뮬레이션

| 함수 | 역할 |
|---|---|
| `mem_init()` | `malloc(256MB)`로 가짜 힙 확보 |
| `mem_sbrk(incr)` | brk를 incr만큼 전진, 이전 brk 반환 |
| `mem_heap_lo()` / `mem_heap_hi()` | 힙 범위 |
| `mem_heapsize()` | 현재 brk - start |
| `mem_reset_brk()` | brk를 start로 리셋 (트레이스 간 초기화) |

시스템 `sbrk()`와 동일한 인터페이스지만, 256MB 고정 버퍼 위에서 동작한다.

---

## 8. 드라이버 검증 항목

| 검증 | 방법 |
|---|---|
| 16바이트 정렬 | `(ptr & 0xf) == 0` |
| 겹침 없음 | 할당 시 모든 live 블록과 범위 교차 검사 |
| Payload 보존 | `expected_byte(id, index)` 패턴 쓰기/읽기 |
| Realloc prefix | `verify_preserved_prefix(ptr, id, old_size, new_size)` |

---

## 9. 트레이스 형식

```
<num_ids> <num_ops>
a <id> <size>     # malloc
f <id>            # free
r <id> <size>     # realloc
```

id는 0-based. 드라이버가 `blocks[id]`, `sizes[id]` 배열로 live 상태를 추적한다.

---

## 10. C vs C++ 구현 차이

| 항목 | C | C++ |
|---|---|---|
| 타입 캐스트 | `(char *)`, `(void **)` | `static_cast`, `reinterpret_cast` |
| bool | `int` (0/1) | `bool` (true/false) |
| 상수 | `#define` | `constexpr` |
| 전역 | `static` | anonymous namespace |
| 링키지 | 기본 | `extern "C"` wrapper |
| 문자열 복사 | `memcpy` | `std::memcpy` |

동일한 알고리즘, 동일한 블록 레이아웃. C++ 트랙은 언어 관용구만 교체.
