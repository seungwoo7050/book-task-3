# 운영체제 완전 가이드

운영체제 학습에서 자주 막히는 지점은 "용어는 많은데 각각이 코드에서 어떻게 보이는지"가 흐릿하다는 점이다. 이 문서는 scheduler, virtual memory, filesystem, synchronization을 작은 실험 프로젝트와 연결해 한 장으로 고정하는 가이드다. 이 문서를 읽고 나면 네 영역 각각에서 "어떤 질문을 해야 하는지"와 "코드에서 어떤 구조가 그 질문에 답하는지"를 연결할 수 있다.

아래 세 질문을 기준으로 읽으면 OS 개념이 훨씬 빨리 정리된다.

1. 이 정책 또는 구조가 **어떤 문제를 해결하려는 것인가?**
2. 그 해결책은 **어떤 tradeoff를 안고 있는가?**
3. **코드나 숫자로 보면 어떤 차이가 나는가?**

---

## 1. Scheduler — 누가 먼저 실행되는가

scheduler는 CPU를 누구에게 언제 얼마나 줄지 정한다. 정책마다 다른 metric을 최적화하기 때문에, 먼저 세 가지 시간을 명확히 구분해야 한다.

### 핵심 메트릭 세 가지

```
arrival=0, burst=4 인 프로세스 P1 기준:

  |-- waiting_time --|-- burst --|
  ^arrival            ^첫 실행    ^completion

waiting_time    = 첫 실행 시작 시점 - arrival 시점
response_time   = 첫 실행 시작 시점 - arrival 시점  (선점형에서도 동일)
turnaround_time = completion 시점   - arrival 시점
```

`turnaround = waiting + burst` 가 항등식이 아닌 이유는 선점형 정책에서 job이 중간에 멈추고 다시 시작하기 때문이다. 비선점형에서는 `waiting + burst = turnaround`가 정확히 성립한다.

### FCFS (First-Come, First-Served)

도착 순서 그대로 실행한다. 가장 단순하지만 **convoy effect**가 생기기 쉽다.

```python
# 도착순 정렬 후 순서대로 실행
pending = sorted(processes, key=lambda p: (p.arrival, p.pid))

# P1: arrival=0 burst=6, P2: arrival=1 burst=2, P3: arrival=2 burst=4
# 실행 순서: P1(0–6) → P2(6–8) → P3(8–12)
#
# waiting_time: P1=0, P2=5, P3=6  avg=3.67
# turnaround:   P1=6, P2=7, P3=10 avg=7.67
#
# convoy effect: P2는 burst=2인데 P1의 burst=6이 끝날 때까지 기다린다.
```

### SJF (Shortest Job First)

burst가 짧은 job을 먼저 실행한다. **이론적으로 평균 waiting time이 최소**지만 미래 burst를 알아야 한다는 가정이 현실적이지 않다.

```python
# ready queue에서 burst가 가장 작은 것을 선택 (비선점형 SJF)
def pick_next(ready_queue):
    return min(ready_queue, key=lambda p: (p.burst, p.pid))

# 선점형 버전(SRTF): t=1에 P2(remaining=2)가 P1(remaining=5)보다 짧아 선점
# → P2가 먼저 완료되어 평균 waiting time이 더 낮아짐
```

### RR (Round-Robin)

time quantum 단위로 CPU를 돌아가며 준다. response time을 낮추기 좋지만 **quantum이 너무 작으면 context switch overhead가 커지고, 너무 크면 FCFS에 가까워진다**.

```python
# quantum=2, P1/P2/P3 모두 t=0에 도착 (burst: P1=6, P2=2, P3=4)

# t=0–2:   P1 실행 (remaining → 4)
# t=2–4:   P2 실행 (remaining → 0, 완료)
# t=4–6:   P3 실행 (remaining → 2)
# t=6–8:   P1 실행 (remaining → 2)
# t=8–10:  P3 실행 (remaining → 0, 완료)
# t=10–12: P1 실행 (remaining → 0, 완료)
#
# response_time: P1=0, P2=2, P3=4  avg=2.00  ← FCFS(avg=?)보다 훨씬 낮음
# waiting_time:  P1=6, P2=2, P3=6  avg=4.67  ← FCFS보다 나쁨
# ⟹ RR은 fairness와 responsiveness를 위해 throughput을 일부 희생한다.
```

### MLFQ (Multi-Level Feedback Queue)

priority queue를 여러 단계로 두고, 오래 실행된 job은 낮은 queue로 강등한다. **interactive job**(짧게 쓰고 I/O wait)은 상위 queue에 남고, CPU-intensive job은 아래로 내려간다.

```
queue 0 (quantum=1)  — 높은 우선순위, 새 job 진입
queue 1 (quantum=2)  — 중간
queue 2 (quantum=4)  — 낮은 우선순위, CPU-bound job

규칙:
  - 새 job은 queue 0에 진입
  - quantum 소진 → 한 단계 아래 queue로 강등
  - I/O 후 복귀 → 원래 queue로 돌아옴
  - boost_interval마다 모든 job → queue 0으로 올려 starvation 방지
```

MLFQ는 burst를 미리 알지 않고도 SJF와 비슷한 효과를 낸다. 단점은 파라미터(queue 수, quantum, boost 간격) 조정이 workload에 따라 달라진다는 것이다.

### 정책 선택 가이드

| 정책 | 최적화 target | 주요 단점 | 적합한 상황 |
|------|--------------|-----------|------------|
| FCFS | 구현 단순성 | convoy effect | 배치, 일괄 처리 |
| SJF | 평균 waiting time | 미래 burst 필요 | 이론적 하한선 비교 |
| RR | response time, fairness | quantum 조정 필요 | time-sharing, 웹 서버 |
| MLFQ | interactive + CPU 혼합 | 파라미터 조정 | 범용 OS |

연결 프로젝트: [`scheduling-simulator`](../../cs-core/study/Operating-Systems-Internals/scheduling-simulator/README.md)

---

## 2. Virtual Memory — page가 frame에 어떻게 매핑되는가

virtual memory는 각 프로세스가 연속되고 큰 주소 공간을 가진 것처럼 보이게 한다. 실제 물리 메모리(frame)는 제한적이고, page 단위로 on-demand loading한다.

### 주소 변환 구조

```
virtual address:  [ VPN (virtual page number) | offset ]
                                  ↓
                          page table lookup
                                  ↓
physical address: [ PFN (physical frame number) | offset ]

page table entry (PTE):
  valid bit     — 이 page가 현재 물리 메모리에 있는가
  dirty bit     — 수정됐는가 (evict 시 디스크에 써야 하는가)
  reference bit — 최근에 접근됐는가 (Clock 알고리즘용)
  PFN           — 매핑된 physical frame 번호
```

valid bit = 0인 page에 접근하면 **page fault**가 발생한다. OS가 끼어들어 비어 있는 frame을 찾고(없으면 교체), 필요한 page를 디스크에서 로드한다.

### Page Replacement 정책

```python
# frame_size=3, 참조 순서: [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]

# FIFO — 가장 오래 전에 들어온 frame을 교체
# frames 변화: [1] [1,2] [1,2,3] F→[2,3,4] F→[3,4,1] F→[4,1,2] F→[1,2,5] ...
# 총 fault: 9회

# LRU — 가장 오래 전에 사용한 frame을 교체
# 최근 사용 기록으로 최소 fault 달성
# 총 fault: 8회  (일반적으로 FIFO보다 적음)

# Clock — reference bit로 LRU를 근사 (second-chance 알고리즘)
# ref=1이면 0으로 초기화하고 건너뜀, ref=0이면 교체
# 구현 단순, LRU에 가까운 성능

# OPT (Belady) — 가장 나중에 다시 쓰일 frame을 교체
# 미래 참조를 알아야 하므로 현실 구현 불가, 이론적 하한선
# 총 fault: 6회
```

**Belady anomaly**: FIFO에서는 frame 수를 늘려도 fault가 오히려 늘어나는 경우가 있다. LRU와 OPT는 이 문제가 없는 **stack property**를 가진다.

### Locality와 Working Set

```
temporal locality:  최근에 쓴 page를 곧 다시 씀 → LRU가 잘 맞음
spatial locality:   현재 쓰는 page 근처를 곧 씀 → prefetching, large page 효과적

working set  = 현재 프로세스가 활발히 사용하는 page 집합
thrashing    = working set보다 frame이 부족해 fault가 폭발적으로 증가하는 상태

thrashing 진단:
  - page fault rate가 급격히 증가
  - CPU utilization이 오히려 낮아짐 (IO 기다리는 시간이 대부분)
  - 해결: 프로세스 수 줄이기, 물리 메모리 추가
```

연결 프로젝트: [`virtual-memory-lab`](../../cs-core/study/Operating-Systems-Internals/virtual-memory-lab/README.md)

---

## 3. Filesystem — 이름이 데이터 블록에 닿는 경로

filesystem은 파일 이름을 inode 번호로 매핑하고, inode가 실제 data block 목록을 가리키는 두 단계 간접참조 구조다.

### inode와 block 구조

```
superblock               — 전체 filesystem 메타데이터 (block size, inode count 등)
inode bitmap             — 어떤 inode 슬롯이 사용 중인가
block bitmap             — 어떤 data block이 사용 중인가
inode table[i]:
    mode, uid, gid, size
    atime, mtime, ctime
    direct_blocks[12]     — 직접 가리키는 data block 번호들
    indirect_block        — block 번호 목록을 담은 block을 가리키는 포인터
    double_indirect_block — 두 단계 간접

data blocks              — 실제 파일 내용 또는 디렉터리 엔트리 목록
```

파일 하나를 읽으려면:
1. 디렉터리 엔트리에서 파일 이름 → inode 번호
2. inode table에서 inode 번호 → block 목록
3. 각 block read

이 과정에서 각 단계가 별도 disk I/O를 유발한다. 그래서 inode와 directory block도 page cache에 올라간다.

### Journaling — crash 이후에도 일관성 유지

파일 write는 원자적이지 않다. data block 쓰기 → inode 업데이트 → bitmap 업데이트 순서 중 어느 시점에 crash가 나도 filesystem이 일관된 상태로 복구돼야 한다.

```
journal write 순서:

  1. journal에 TxB (transaction begin) 기록
  2. journal에 변경할 내용 기록 (inode, bitmap, data block)
  3. journal에 TxE (transaction end / commit) 기록       ← 이 시점이 commit point
  4. 실제 disk의 대상 위치에 데이터 반영 (checkpoint)
  5. journal에서 해당 transaction 삭제

recovery 규칙:
  - TxE 있음 → replay   (checkpoint가 아직 안 됐을 수 있으므로 다시 적용)
  - TxE 없음 → discard  (commit 전 crash → prepared entry는 무효, 버린다)
```

**metadata-only journaling** (ext3 기본 모드): data block은 먼저 직접 쓰고, inode/bitmap update만 journal로 보호한다. full journaling보다 빠르지만 crash 시 data block이 갱신됐는데 inode가 아직 가리키지 않을 수 있다.

```python
# Python으로 표현한 mini filesystem의 기본 구조
@dataclass
class Inode:
    ino: int
    size: int
    block_refs: list[int]   # 할당된 block 번호들

@dataclass
class JournalEntry:
    tx_id: int
    changes: list          # 변경할 inode/bitmap/block 내용
    committed: bool        # TxE가 기록됐는가

# crash recovery: committed=True인 entry만 replay
for entry in journal:
    if entry.committed:
        apply_to_disk(entry.changes)
```

연결 프로젝트: [`filesystem-mini-lab`](../../cs-core/study/Operating-Systems-Internals/filesystem-mini-lab/README.md)

---

## 4. Synchronization — shared state를 어떻게 안전하게 바꾸는가

여러 thread가 같은 데이터를 동시에 바꾸면 **race condition**이 생긴다. synchronization primitive는 이 문제를 다루는 도구들이다.

### 세 primitive 비교

```c
// mutex — 한 번에 한 thread만 critical section 접근
pthread_mutex_lock(&lock);
counter++;                          // critical section
pthread_mutex_unlock(&lock);

// semaphore — permit 수만큼만 동시 진입 허용
// sem_init(&sem, 0, N) → N개 동시 접근 허용
sem_wait(&sem);                     // permit 획득 (0이면 block)
use_shared_resource();
sem_post(&sem);                     // permit 반환

// condition variable — 조건이 만족될 때까지 sleep
pthread_mutex_lock(&lock);
while (buffer_full()) {             // if 대신 while: spurious wakeup 방어
    pthread_cond_wait(&not_full, &lock);  // lock 해제 + sleep
}
produce_item();
pthread_cond_signal(&not_empty);
pthread_mutex_unlock(&lock);
```

`while` 조건으로 다시 확인하는 이유는 **spurious wakeup** 때문이다. `signal`을 받아 깨어났어도 다른 thread가 먼저 조건을 소비했을 수 있다. `if`로 쓰면 조건이 거짓인 상태에서 진행하는 버그가 생긴다.

### Deadlock 발생 조건과 예방

아래 네 조건이 **동시에** 성립할 때 deadlock이 생긴다.

```
1. mutual exclusion: 자원을 한 번에 하나만 점유
2. hold and wait:    자원을 들고 있으면서 다른 자원을 기다림
3. no preemption:    점유한 자원을 강제로 빼앗을 수 없음
4. circular wait:    A→B, B→A 같은 순환 대기

예방 전략 — 위 네 조건 중 하나를 깬다:
  lock ordering:    항상 같은 순서로 lock 획득 → circular wait 제거
  try-lock+backoff: 실패하면 들고 있던 lock 해제 후 재시도 → hold and wait 완화
  timeout:          일정 시간 내 lock 획득 실패 시 포기 → starvation도 완화
```

### Livelock과 Starvation

```
livelock:   thread들이 서로 양보하면서 진행이 없는 상태
            (deadlock과 달리 thread는 계속 실행 중)
starvation: 우선순위가 낮은 thread가 계속 선점당해 자원을 못 받는 상태
            MLFQ의 boost_interval이 바로 starvation 방지 기법
```

### 테스트에서 timing보다 invariant를 먼저 본다

concurrency 테스트는 timing에 의존하면 flaky해진다. 대신 **불변 조건(invariant)**이 항상 성립하는지를 검증한다.

```python
# counter 테스트 — 결과값이 정확한가
def test_concurrent_counter():
    counter = SharedCounter()
    threads = [Thread(target=counter.increment, args=(1000,)) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert counter.value == 10_000     # invariant: 정확히 10,000

# semaphore 테스트 — permit ceiling이 지켜지는가
def test_semaphore_ceiling():
    sem = BoundedSemaphore(N=3)
    max_concurrent = track_max_concurrent(sem, workers=10)
    assert max_concurrent <= 3         # invariant: 동시 진입은 항상 3 이하

# producer-consumer 테스트 — buffer under/overflow 없음
def test_producer_consumer():
    run_scenario(producers=3, consumers=2, items=500)
    assert no_underflow_occurred()     # invariant: 빈 buffer에서 꺼내지 않음
    assert no_overflow_occurred()      # invariant: 꽉 찬 buffer에 넣지 않음
```

연결 프로젝트: [`synchronization-contention-lab`](../../cs-core/study/Operating-Systems-Internals/synchronization-contention-lab/README.md)

---

## 빠른 참조

| 영역 | 핵심 질문 | 주요 개념 | 흔한 실수 |
|------|----------|----------|---------|
| Scheduler | 누가 먼저 돌았는가, 누가 오래 기다렸는가? | waiting / response / turnaround time | response time과 waiting time 혼동 |
| Virtual Memory | 어떤 page가 frame에 남았는가, 왜 fault가 났는가? | PTE valid/dirty/ref bit, fault, locality | Belady anomaly가 LRU에도 발생한다고 오해 |
| Filesystem | inode와 block이 어떻게 할당됐는가, crash 뒤 replay vs discard? | inode, bitmap, journal TxB/TxE, checkpoint | TxE 없으면 replay라고 오해 (정답: discard) |
| Synchronization | 어떤 invariant를 지켜야 하고, wait는 어디서 발생하는가? | mutex, semaphore, condvar, deadlock | cond_wait를 `if`로 감싸면 spurious wakeup에 취약 |

```
정책 선택 요약:
  scheduler:        MLFQ (범용) > RR (interactive) > SJF (이론 기준) > FCFS (배치)
  page replacement: OPT (이론 기준) > LRU (현실 최선) > Clock (근사) > FIFO (단순)
  sync primitive:   mutex (배타 접근), semaphore (permit 제한), condvar (조건 대기)
```
