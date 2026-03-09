# Malloc Lab — 회고

## 가장 어려웠던 것

블록 포인터 산술이다. `header_of`, `footer_of`, `next_block`, `previous_block` — 네 함수가 전체 allocator의 기초인데, 이 중 하나라도 틀리면 나머지 모든 연산이 silent하게 깨진다. Segfault가 나면 그나마 다행이고, heap corruption이 몇 연산 뒤에야 드러나는 경우가 훨씬 디버깅이 힘들다.

특히 "block 포인터는 header가 아니라 payload 시작점"이라는 규약을 일관되게 지키는 것이 중요했다. C에서는 이런 규약을 타입 시스템이 강제하지 않으므로 개발자가 머릿속에서 추적해야 한다.

---

## 설계 판단의 결과

### Explicit free list는 올바른 선택이었다

Implicit list 대비:
- 탐색이 free 블록 수에만 비례하므로 mixed.rep 같은 시나리오에서 확실히 빠르다
- 코드량은 `add_to_free_list` / `remove_from_free_list` 두 함수가 추가되는 정도

단점은 최소 블록 크기가 32바이트로 올라간다는 것 (free-list 포인터 16바이트 + header/footer 16바이트). 작은 할당이 많으면 internal fragmentation이 implicit보다 심해질 수 있다. 하지만 이 프로젝트의 트레이스에서는 문제가 되지 않았다.

### Eager coalescing은 정답

free 시점에 즉시 병합하면 힙이 항상 "인접한 free 블록이 없는" 정규 형태를 유지한다. Deferred coalescing을 쓰면 throughput이 올라갈 수 있지만, 힙 상태를 추론하기가 급격히 어려워진다. 학습 목적으로는 eager가 확실히 맞다.

---

## In-place realloc의 가치

realloc에서 "다음 블록이 free이고 합치면 충분한 경우" in-place로 성장하는 경로를 추가한 것이 이 allocator에서 가장 실질적인 최적화다. 이 경로가 없으면 realloc은 항상 malloc-memcpy-free가 되어:

1. 불필요한 memcpy 비용
2. 원래 블록과 새 블록이 동시에 살아있는 순간의 peak heap 증가

실제 프로그램에서 realloc은 배열 확장(vector grow)에 빈번히 사용되는데, 연속 확장이 대부분 in-place로 해결되면 throughput과 utilization이 동시에 개선된다.

---

## 드라이버 강화의 의미

CMU 원본 드라이버는 주로 segfault / 정렬 위반만 잡는다. 이 스터디 버전 드라이버는:

- **결정적 패턴 채우기**: `expected_byte(id, index)` — 각 블록에 id와 offset 기반 패턴을 쓰고, free/realloc 전에 검증
- **겹침 감지**: 모든 할당 시 live 블록 전체와 범위 교차 검사
- **realloc prefix 보존**: 이동 후 이전 payload의 보존된 접두어를 바이트 단위 비교

이런 드라이버가 있으니 allocator 버그가 "이상한 동작"이 아니라 "trace X, op N에서 에러"로 즉시 좁혀진다. 커스텀 드라이버를 만든 투자가 디버깅 시간을 크게 절약했다.

---

## 트레이스 설계의 교훈

4개 트레이스를 직접 작성한 것도 큰 배움이었다:

- **basic.rep**: malloc/free 기본 경로만 확인. allocator가 "돌아가기는 하는가".
- **coalesce.rep**: 연속 해제 후 대형 할당. 병합이 제대로 작동하지 않으면 여기서 실패.
- **realloc.rep**: NULL → 성장 → 축소 → zero-size 전체 경로. realloc 계약의 모든 엣지 케이스.
- **mixed.rep**: 세 연산이 뒤섞인 현실적 시나리오. 개별 트레이스를 통과해도 여기서 실패할 수 있다.

"테스트를 만드는 것 자체가 명세를 이해하는 과정"이라는 통찰을 다시 확인했다.

---

## 여기서 더 나아간다면

이 allocator를 기반으로 확장할 수 있는 방향:

1. **Segregated free list**: 크기 클래스별 리스트로 탐색 O(1) 근접
2. **Footer 제거 (allocated 블록)**: header에 prev-alloc bit를 추가하면 할당 블록의 footer를 없앨 수 있다. 8바이트 절약.
3. **Best-fit 또는 next-fit**: utilization / locality 트레이드오프
4. **Mini-block**: 16바이트 이하 요청에 대한 특수 경로

하지만 이 프로젝트의 학습 목표 — 블록 산술, 경계 태그, 리스트 조작, 병합 정합성 — 는 explicit free list로 충분히 달성됐다. 더 복잡한 구조는 필요할 때 추가하면 된다.

---

## 현재 성능

```
avg_util = 0.077
C throughput  ≈ 4,691,933 ops/s
C++ throughput ≈ 5,033,165 ops/s
```

utilization이 낮은 것은 트레이스가 의도적으로 작고 sparse하기 때문이다 (peak_live 대비 peak_heap이 커지는 구조). 대형 트레이스에서는 다른 값이 나올 것이다. 중요한 것은 errors=0이다 — 정합성이 보장된 allocator 위에서 최적화를 쌓아야 의미가 있다.
