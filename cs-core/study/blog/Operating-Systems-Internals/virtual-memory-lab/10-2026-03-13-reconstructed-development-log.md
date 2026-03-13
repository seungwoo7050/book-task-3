# Virtual Memory Lab 재구성 개발 로그

`virtual-memory-lab`는 page reference trace를 따라가며 replacement policy와 locality가 page fault 수를 어떻게 바꾸는지 보여 주는 실험이다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

trace loader와 공통 simulator를 먼저 세운 뒤, replacement policy와 dirty-page/writeback 규칙이 결과 표에 어떻게 반영되는지 따라간다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: trace와 frame state를 읽는 공통 루프를 먼저 만든다 — `python/src/os_virtual_memory/core.py`
- Phase 2: replacement policy와 writeback 차이를 별도 규칙으로 드러낸다 — `python/src/os_virtual_memory/core.py`
- Phase 3: trace replay와 summary metric으로 실험을 닫는다 — `python/src/os_virtual_memory/cli.py`, `python/tests/test_os_virtual_memory.py`

## Phase 1. trace와 frame state를 읽는 공통 루프를 먼저 만든다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 page replacement 비교도 먼저 필요한 것은 trace와 frame state를 어떤 형식으로 표현할지다.

처음에는 LRU/FIFO/Clock/OPT를 바로 구현하기보다 trace parsing과 공통 simulate loop를 먼저 고정하는 편이 훨씬 덜 흔들릴 거라고 봤다. 그런데 실제로 글의 중심이 된 조치는 `load_trace`, `simulate_policy`, frame rendering helper를 먼저 세워 공통 실험면을 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `python/src/os_virtual_memory/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: 공통 루프가 있으니 정책 차이를 좁은 함수 범위에서 설명할 수 있다.

### 이 장면을 고정하는 코드 — `load_trace` (`python/src/os_virtual_memory/core.py:55`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

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

`load_trace`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 vm 실험의 핵심도 policy 이름이 아니라 모두가 같은 trace 위에서 같은 frame state를 공유한다는 사실이었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 policy-specific 선택 로직과 dirty page 처리로 넘어간다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 VM 실험의 핵심도 policy 이름이 아니라 모두가 같은 trace 위에서 같은 frame state를 공유한다는 사실이었다.

그래서 다음 장면에서는 policy-specific 선택 로직과 dirty page 처리로 넘어간다.

## Phase 2. replacement policy와 writeback 차이를 별도 규칙으로 드러낸다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 Clock/OPT 선택 함수와 dirty page summary가 이 lab의 실제 개념 전환점이다.

처음에는 policy 차이를 단순 fault count로만 설명하면 locality와 writeback 규칙의 차이가 묻힐 것이라고 판단했다. 그런데 실제로 글의 중심이 된 조치는 `_clock_select`, `_opt_select`, `render_summary`를 중심으로 eviction과 dirty-page signal을 동시에 보여 주도록 정리했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `python/src/os_virtual_memory/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: 정책 helper와 summary renderer가 같은 판단 전환점을 보존한다.

### 이 장면을 고정하는 코드 — `_clock_select` (`python/src/os_virtual_memory/core.py:129`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

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

`_clock_select`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 vm 설명은 어느 페이지를 쫓아냈는가보다, 왜 그 선택이 fault/writeback 수치로 이어졌는지까지 같이 말할 때 완성됐다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 demo trace와 summary 출력을 통해 결과를 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 VM 설명은 어느 페이지를 쫓아냈는가보다, 왜 그 선택이 fault/writeback 수치로 이어졌는지까지 같이 말할 때 완성됐다.

그래서 다음 장면에서는 demo trace와 summary 출력을 통해 결과를 닫는다.

## Phase 3. trace replay와 summary metric으로 실험을 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 VM lab도 결국 외부에서 읽히는 것은 trace별 fault/writeback 차이와 frame replay다.

처음에는 CLI가 남아 있어야 locality와 replacement policy 설명이 표 한 장으로 축약되지 않을 것이라고 봤다. 그런데 실제로 글의 중심이 된 조치는 `make run-demo`와 `render_replay` surface를 통해 locality/dirty trace를 다시 재생하고 요약하게 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `python/src/os_virtual_memory/cli.py`, `python/tests/test_os_virtual_memory.py`
- CLI: `make test && make run-demo`
- 검증 신호: 현재 demo 출력이 정책별 차이를 수치로 남긴다.

### 이 장면을 고정하는 코드 — `main` (`python/src/os_virtual_memory/cli.py:22`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

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

`main`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 메모리 관리 개념도 trace 기반 replay가 있으면 구현과 개념 note가 자연스럽게 붙는다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 common trace loop -> policy selection -> replay summary 순서로 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 메모리 관리 개념도 trace 기반 replay가 있으면 구현과 개념 note가 자연스럽게 붙는다.

그래서 다음 장면에서는 common trace loop -> policy selection -> replay summary 순서로 닫는다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

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

## 이번에 남은 질문

- 개념 축: `dirty pages and writeback`, `locality and faults`, `replacement policies`
- 대표 테스트/fixture: `python/tests/test_os_virtual_memory.py`
- 다음 질문: 최종 글은 common trace loop -> policy selection -> replay summary 순서로 닫는다.
