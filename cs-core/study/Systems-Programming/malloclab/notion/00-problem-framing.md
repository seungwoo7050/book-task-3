# Malloc Lab — 문제 정의와 범위

## 어떤 문제인가

malloc(3)을 직접 만든다. `mm_init`, `mm_malloc`, `mm_free`, `mm_realloc` — 네 함수가 계약 전부다. `memlib.c`가 제공하는 가짜 힙(256MB 고정 mmap) 위에서 동작해야 하고, 시스템 `malloc`을 호출하는 것은 금지다. 반환하는 모든 포인터는 16바이트 정렬이어야 한다.

이 랩의 핵심 긴장은 **공간 효율(utilization)** 과 **시간 효율(throughput)** 사이의 트레이드오프다. 블록을 잘게 쪼개면 낭비가 줄지만 탐색이 느려지고, 크게 남기면 빠르지만 fragmentation이 심해진다.

---

## 무엇이 주어지는가

| 구성 요소 | 역할 |
|---|---|
| `memlib.c` / `memlib.h` | 힙 시뮬레이션. `mem_sbrk(incr)`가 유일한 성장 수단 |
| `problem/code/mm.c` | TODO만 있는 스켈레톤 |
| `problem/script/mdriver.c` | 트레이스 기반 검증 드라이버 |
| `problem/data/traces/*.rep` | 4개 트레이스 세트 |

트레이스 형식:

```
<num_ids> <num_ops>
a <id> <size>     # malloc
f <id>            # free
r <id> <size>     # realloc
```

드라이버는 각 할당마다 결정적 패턴을 채우고, free/realloc 시 그 패턴이 보존되었는지 검증한다. 정렬, 겹침, payload 보존 — 세 가지를 모두 체크한다.

---

## 트레이스 구성

- **basic.rep** (8 ids, 12 ops): malloc/free 기본 동작
- **coalesce.rep** (10 ids, 18 ops): 연속 free 후 대형 할당으로 병합 압박
- **realloc.rep** (6 ids, 14 ops): `realloc(NULL, n)`, 성장, 축소, `realloc(ptr, 0)`
- **mixed.rep** (12 ids, 22 ops): malloc/free/realloc 섞인 혼합 시나리오

---

## 이 랩이 어려운 이유

1. **블록 산술**: 헤더, 푸터, 페이로드, 정렬 패딩이 모두 명시적 포인터 연산으로 표현된다. 한 바이트라도 어긋나면 silent corruption.
2. **경계 태그 일관성**: 할당/해제/분할/병합 중 어디 하나라도 header-footer 쌍을 놓치면 이후 모든 순회가 깨진다.
3. **Free-list 동기화**: 블록을 병합할 때 이웃을 먼저 리스트에서 제거하고, 결과를 다시 삽입하는 순서가 정확해야 한다.
4. **Realloc 정합성**: 이전 payload 데이터를 보존하면서 블록을 원위치 성장시키거나 이동해야 한다. 드라이버가 바이트 단위로 검증한다.

---

## 내 스터디 버전의 차이점

원래 CMU 랩은 `mdriver`가 대형 트레이스(amptjp, binary, random 등)를 돌리며 점수를 매기지만, 이 스터디 버전은:

- 트레이스를 직접 작성하여 각 시나리오를 분리 테스트할 수 있게 만들었다
- 드라이버가 payload 패턴 검증 + 겹침 감지를 수행하도록 강화했다
- `problem/` 스켈레톤과 `c/`/`cpp/` 완성 구현을 명확히 분리했다
