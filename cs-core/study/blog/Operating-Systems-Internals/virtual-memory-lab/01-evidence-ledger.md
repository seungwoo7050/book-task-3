# Virtual Memory Lab Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`virtual-memory-lab`는 page reference trace를 따라가며 replacement policy와 locality가 page fault 수를 어떻게 바꾸는지 보여 주는 실험이다. 구현의 중심은 `python`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `python/src/os_virtual_memory/__init__.py`, `python/src/os_virtual_memory/__main__.py`, `python/src/os_virtual_memory/cli.py`, `python/src/os_virtual_memory/core.py`다. 검증 표면은 `python/tests/test_os_virtual_memory.py`와 `make test && make run-demo`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `dirty pages and writeback`, `locality and faults`, `replacement policies`이다.

## Git History Anchor

- `2026-03-11	0cccd64	feat: add new project in cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - trace와 frame state를 읽는 공통 루프를 먼저 만든다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 page replacement 비교도 먼저 필요한 것은 trace와 frame state를 어떤 형식으로 표현할지다.

그때 세운 가설은 LRU/FIFO/Clock/OPT를 바로 구현하기보다 trace parsing과 공통 simulate loop를 먼저 고정하는 편이 훨씬 덜 흔들릴 거라고 봤다. 실제 조치는 `load_trace`, `simulate_policy`, frame rendering helper를 먼저 세워 공통 실험면을 만들었다.

- 정리해 둔 근거:
- 변경 단위: `python/src/os_virtual_memory/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: 공통 루프가 있으니 정책 차이를 좁은 함수 범위에서 설명할 수 있다.
- 새로 배운 것: VM 실험의 핵심도 policy 이름이 아니라 모두가 같은 trace 위에서 같은 frame state를 공유한다는 사실이었다.

### 코드 앵커 — `load_trace` (`python/src/os_virtual_memory/core.py:55`)

```python
def load_trace(path: str | Path) -> list[PageAccess]:
    accesses: list[PageAccess] = []
    for raw_line in Path(path).read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        mode, page = line.split()
        accesses.append(PageAccess(mode=mode, page=int(page)))
    return accesses
```

이 조각은 공통 루프가 있으니 정책 차이를 좁은 함수 범위에서 설명할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `load_trace`를 읽고 나면 다음 장면이 왜 policy-specific 선택 로직과 dirty page 처리로 넘어간다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `simulate_policy` (`python/src/os_virtual_memory/core.py:66`)

```python
def simulate_policy(
    policy: str,
    accesses: Iterable[PageAccess],
    frame_count: int,
) -> PolicyResult:
    if policy not in POLICIES:
        raise ValueError(f"unknown policy: {policy}")
    trace = list(accesses)
    frames: list[Frame] = []
    steps: list[ReplayStep] = []
    clock_hand = 0
```

이 조각은 공통 루프가 있으니 정책 차이를 좁은 함수 범위에서 설명할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `simulate_policy`를 읽고 나면 다음 장면이 왜 policy-specific 선택 로직과 dirty page 처리로 넘어간다로 이어지는지도 한 번에 보인다.

다음 단계에서는 policy-specific 선택 로직과 dirty page 처리로 넘어간다.

## 2. Phase 2 - replacement policy와 writeback 차이를 별도 규칙으로 드러낸다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 Clock/OPT 선택 함수와 dirty page summary가 이 lab의 실제 개념 전환점이다.

그때 세운 가설은 policy 차이를 단순 fault count로만 설명하면 locality와 writeback 규칙의 차이가 묻힐 것이라고 판단했다. 실제 조치는 `_clock_select`, `_opt_select`, `render_summary`를 중심으로 eviction과 dirty-page signal을 동시에 보여 주도록 정리했다.

- 정리해 둔 근거:
- 변경 단위: `python/src/os_virtual_memory/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: 정책 helper와 summary renderer가 같은 판단 전환점을 보존한다.
- 새로 배운 것: VM 설명은 어느 페이지를 쫓아냈는가보다, 왜 그 선택이 fault/writeback 수치로 이어졌는지까지 같이 말할 때 완성됐다.

### 코드 앵커 — `_clock_select` (`python/src/os_virtual_memory/core.py:129`)

```python
def _clock_select(frames: list[Frame], hand: int) -> tuple[int, int]:
    while True:
        frame = frames[hand]
        if frame.referenced:
            frame.referenced = False
            hand = (hand + 1) % len(frames)
            continue
        victim = hand
        hand = (hand + 1) % len(frames)
        return victim, hand
```

이 조각은 정책 helper와 summary renderer가 같은 판단 전환점을 보존한다는 설명이 실제로 어디서 나오는지 보여 준다. `_clock_select`를 읽고 나면 다음 장면이 왜 demo trace와 summary 출력을 통해 결과를 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `_opt_select` (`python/src/os_virtual_memory/core.py:141`)

```python
def _opt_select(frames: list[Frame], trace: list[PageAccess], start: int) -> int:
    future_pages = [access.page for access in trace[start:]]
    distances: list[tuple[int, int]] = []
    for index, frame in enumerate(frames):
        if frame.page not in future_pages:
            return index
        distances.append((future_pages.index(frame.page), index))
    return max(distances)[1]
```

이 조각은 정책 helper와 summary renderer가 같은 판단 전환점을 보존한다는 설명이 실제로 어디서 나오는지 보여 준다. `_opt_select`를 읽고 나면 다음 장면이 왜 demo trace와 summary 출력을 통해 결과를 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 demo trace와 summary 출력을 통해 결과를 닫는다.

## 3. Phase 3 - trace replay와 summary metric으로 실험을 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 VM lab도 결국 외부에서 읽히는 것은 trace별 fault/writeback 차이와 frame replay다.

그때 세운 가설은 CLI가 남아 있어야 locality와 replacement policy 설명이 표 한 장으로 축약되지 않을 것이라고 봤다. 실제 조치는 `make run-demo`와 `render_replay` surface를 통해 locality/dirty trace를 다시 재생하고 요약하게 만들었다.

- 정리해 둔 근거:
- 변경 단위: `python/src/os_virtual_memory/cli.py`, `python/tests/test_os_virtual_memory.py`
- CLI: `make test && make run-demo`
- 검증 신호: 현재 demo 출력이 정책별 차이를 수치로 남긴다.
- 새로 배운 것: 메모리 관리 개념도 trace 기반 replay가 있으면 구현과 개념 note가 자연스럽게 붙는다.

### 코드 앵커 — `main` (`python/src/os_virtual_memory/cli.py:22`)

```python
def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    trace = load_trace(args.trace)
    policies = POLICIES if args.policy == "all" else (args.policy,)
    results = [simulate_policy(policy, trace, args.frames) for policy in policies]
    if args.replay:
        for result in results:
            print(f"[{result.policy}]")
            print(render_replay(result))
    print(render_summary(results))
    return 0
```

이 조각은 현재 demo 출력이 정책별 차이를 수치로 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `main`를 읽고 나면 다음 장면이 왜 common trace loop -> policy selection -> replay summary 순서로 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `test_dirty_evictions_counted` (`python/tests/test_os_virtual_memory.py:29`)

```python
def test_dirty_evictions_counted() -> None:
    trace = load_trace(TRACE_DIR / "dirty.trace")
    fifo = simulate_policy("fifo", trace, 2)
    assert fifo.dirty_evictions == 1
```

이 조각은 현재 demo 출력이 정책별 차이를 수치로 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `test_dirty_evictions_counted`를 읽고 나면 다음 장면이 왜 common trace loop -> policy selection -> replay summary 순서로 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 common trace loop -> policy selection -> replay summary 순서로 닫는다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/virtual-memory-lab/problem && make test && make run-demo)
```

```text
9    R3 fault       1    no [2, 3, 5]
 10    R4 fault       3    no [2, 4, 5]
 11    R5   hit       -    no [2, 4, 5]
policy frames faults hits dirty_evictions
 fifo      3      9    3               0
  lru      3     10    2               0
clock      3      9    3               0
  opt      3      7    5               0
```
