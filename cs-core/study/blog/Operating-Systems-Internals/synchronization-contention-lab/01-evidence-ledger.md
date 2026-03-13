# Synchronization Contention Lab Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`synchronization-contention-lab`는 mutex, semaphore, condition variable이 서로 다른 contention pattern에서 correctness와 timing을 어떻게 드러내는지 보여 주는 C 실험이다. 구현의 중심은 `c`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `c/src/contention_lab.c`, `c/src/main.c`다. 검증 표면은 `c/tests/test_cases.sh`와 `make test && make run-demo`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `correctness before timing`, `mutex semaphore condvar`, `scenario invariants`이다.

## Git History Anchor

- `2026-03-11	0cccd64	feat: add new project in cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - shared-state 시나리오를 먼저 만든다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 동기화 실험은 primitive보다 먼저 어떤 shared state를 보호하려는지 보여 줘야 한다.

그때 세운 가설은 mutex/semaphore/condvar를 바로 비교하는 것보다 counter/gate/buffer 시나리오를 먼저 세우는 편이 각 primitive의 역할을 설명하기 쉽다고 판단했다. 실제 조치는 `run_counter_scenario`, `run_gate_scenario`, `run_buffer_scenario`로 shared-state 실험면을 먼저 만들었다.

- 정리해 둔 근거:
- 변경 단위: `c/src/contention_lab.c`
- CLI: `make test && make run-demo`
- 검증 신호: 시나리오 분리가 있어야 primitive 차이를 기능적으로 비교할 수 있다.
- 새로 배운 것: 동기화는 도구 이름이 아니라 어떤 invariant를 지켜야 하는지로 읽힐 때 더 명확했다.

### 코드 앵커 — `run_counter_scenario` (`c/src/contention_lab.c:163`)

```c
int run_counter_scenario(int threads, int iterations, lab_metrics_t *metrics) {
    memset(metrics, 0, sizeof(*metrics));
    metrics->scenario = "counter";
    metrics->expected_count = (long)threads * (long)iterations;
```

이 조각은 시나리오 분리가 있어야 primitive 차이를 기능적으로 비교할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `run_counter_scenario`를 읽고 나면 다음 장면이 왜 primitive 선택과 correctness reasoning으로 넘어간다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `run_gate_scenario` (`c/src/contention_lab.c:196`)

```c
int run_gate_scenario(int threads, int iterations, lab_metrics_t *metrics) {
    memset(metrics, 0, sizeof(*metrics));
    metrics->scenario = "gate";
    metrics->permit_limit = threads >= 4 ? threads / 4 : 1;
    metrics->expected_count = (long)threads * (long)iterations;
```

이 조각은 시나리오 분리가 있어야 primitive 차이를 기능적으로 비교할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `run_gate_scenario`를 읽고 나면 다음 장면이 왜 primitive 선택과 correctness reasoning으로 넘어간다로 이어지는지도 한 번에 보인다.

다음 단계에서는 primitive 선택과 correctness reasoning으로 넘어간다.

## 2. Phase 2 - primitive 선택을 timing이 아니라 invariant 기준으로 설명한다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 이 lab의 핵심은 누가 더 빠른가보다 어떤 primitive가 어떤 조건을 안전하게 표현하는가에 있다.

그때 세운 가설은 동기화 비교가 벤치마크 놀이로 흐르지 않게 correctness-before-timing 원칙을 코드와 docs 모두에 남겨야 한다고 봤다. 실제 조치는 mutex, semaphore, condvar를 시나리오별로 배치하고, 출력 메트릭은 correctness를 통과한 뒤에만 의미가 있도록 정리했다.

- 정리해 둔 근거:
- 변경 단위: `c/src/contention_lab.c`, `docs/concepts/correctness-before-timing.md`
- CLI: `make test && make run-demo`
- 검증 신호: docs concept와 시나리오 함수가 같은 전환점을 공유한다.
- 새로 배운 것: 동기화 primitive는 성능 옵션이 아니라 shared state invariant를 표현하는 문법이라는 점이 분명해졌다.

### 코드 앵커 — `print_metrics` (`c/src/contention_lab.c:309`)

```c
void print_metrics(const lab_metrics_t *metrics) {
    printf("scenario=%s\n", metrics->scenario);
    printf("ok=%d\n", metrics->ok);
    printf("elapsed_ms=%ld\n", metrics->elapsed_ms);
    printf("wait_events=%ld\n", metrics->wait_events);
    printf("final_count=%ld\n", metrics->final_count);
    printf("expected_count=%ld\n", metrics->expected_count);
    printf("max_concurrency=%d\n", metrics->max_concurrency);
    printf("permit_limit=%d\n", metrics->permit_limit);
    printf("produced=%ld\n", metrics->produced);
    printf("consumed=%ld\n", metrics->consumed);
    printf("max_occupancy=%d\n", metrics->max_occupancy);
```

이 조각은 docs concept와 시나리오 함수가 같은 전환점을 공유한다는 설명이 실제로 어디서 나오는지 보여 준다. `print_metrics`를 읽고 나면 다음 장면이 왜 shell test와 demo scenario로 전 과정을 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `# Correctness Before Timing` (`docs/concepts/correctness-before-timing.md:1`)

```markdown
# Correctness Before Timing

## 왜 timing을 테스트 기준으로 쓰지 않는가

contention benchmark는 같은 머신에서도 run마다 시간이 흔들린다. scheduler noise, background load, CPU frequency 변화만으로도 값이 쉽게 달라진다.
```

이 조각은 docs concept와 시나리오 함수가 같은 전환점을 공유한다는 설명이 실제로 어디서 나오는지 보여 준다. `# Correctness Before Timing`를 읽고 나면 다음 장면이 왜 shell test와 demo scenario로 전 과정을 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 shell test와 demo scenario로 전 과정을 닫는다.

## 3. Phase 3 - self-owned shell test와 demo binary로 검증을 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 동기화 실험은 재현 가능한 시나리오 출력이 있어야 reasoning이 추상으로 남지 않는다.

그때 세운 가설은 shell harness와 demo binary를 같이 남기면 primitive별 차이를 다시 확인하기 쉬울 것이라고 판단했다. 실제 조치는 `test_cases.sh`와 `problem/make run-demo`를 통해 counter/gate/buffer 결과를 반복 실행 가능하게 만들었다.

- 정리해 둔 근거:
- 변경 단위: `c/tests/test_cases.sh`, `c/src/main.c`
- CLI: `make test && make run-demo`
- 검증 신호: shell test와 demo 출력이 마지막 검증 신호를 남긴다.
- 새로 배운 것: OS 내부 주제도 작은 demo surface가 있으면 개념 note와 코드가 같은 문서 안에서 연결된다.

### 코드 앵커 — `main` (`c/src/main.c:11`)

```c
int main(int argc, char **argv) {
    const char *scenario = NULL;
    int threads = 0;
    int iterations = 0;
```

이 조각은 shell test와 demo 출력이 마지막 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `main`를 읽고 나면 다음 장면이 왜 scenario design -> invariant choice -> demo verification 순서로 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `extract` (`c/tests/test_cases.sh:7`)

```bash
extract() {
  local key="$1"
  awk -F= -v k="$key" '$1 == k { print $2 }'
}
```

이 조각은 shell test와 demo 출력이 마지막 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `extract`를 읽고 나면 다음 장면이 왜 scenario design -> invariant choice -> demo verification 순서로 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 scenario design -> invariant choice -> demo verification 순서로 닫는다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/synchronization-contention-lab/problem && make test && make run-demo)
```

```text
max_concurrency=0
permit_limit=0
produced=20000
consumed=20000
max_occupancy=8
capacity=8
underflow=0
overflow=0
```
