# Synchronization Contention Lab 재구성 개발 로그

`synchronization-contention-lab`는 mutex, semaphore, condition variable이 서로 다른 contention pattern에서 correctness와 timing을 어떻게 드러내는지 보여 주는 C 실험이다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

counter/gate/buffer 세 시나리오를 먼저 세우고, mutex/semaphore/condvar가 각 시나리오에서 무엇을 보장하는지 따라간다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: shared-state 시나리오를 먼저 만든다 — `c/src/contention_lab.c`
- Phase 2: primitive 선택을 timing이 아니라 invariant 기준으로 설명한다 — `c/src/contention_lab.c`, `docs/concepts/correctness-before-timing.md`
- Phase 3: self-owned shell test와 demo binary로 검증을 닫는다 — `c/tests/test_cases.sh`, `c/src/main.c`

## Phase 1. shared-state 시나리오를 먼저 만든다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 동기화 실험은 primitive보다 먼저 어떤 shared state를 보호하려는지 보여 줘야 한다.

처음에는 mutex/semaphore/condvar를 바로 비교하는 것보다 counter/gate/buffer 시나리오를 먼저 세우는 편이 각 primitive의 역할을 설명하기 쉽다고 판단했다. 그런데 실제로 글의 중심이 된 조치는 `run_counter_scenario`, `run_gate_scenario`, `run_buffer_scenario`로 shared-state 실험면을 먼저 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/contention_lab.c`
- CLI: `make test && make run-demo`
- 검증 신호: 시나리오 분리가 있어야 primitive 차이를 기능적으로 비교할 수 있다.

### 이 장면을 고정하는 코드 — `run_counter_scenario` (`c/src/contention_lab.c:163`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

```c
int run_counter_scenario(int threads, int iterations, lab_metrics_t *metrics) {
    memset(metrics, 0, sizeof(*metrics));
    metrics->scenario = "counter";
    metrics->expected_count = (long)threads * (long)iterations;
```

`run_counter_scenario`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 동기화는 도구 이름이 아니라 어떤 invariant를 지켜야 하는지로 읽힐 때 더 명확했다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 primitive 선택과 correctness reasoning으로 넘어간다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 동기화는 도구 이름이 아니라 어떤 invariant를 지켜야 하는지로 읽힐 때 더 명확했다.

그래서 다음 장면에서는 primitive 선택과 correctness reasoning으로 넘어간다.

## Phase 2. primitive 선택을 timing이 아니라 invariant 기준으로 설명한다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 이 lab의 핵심은 누가 더 빠른가보다 어떤 primitive가 어떤 조건을 안전하게 표현하는가에 있다.

처음에는 동기화 비교가 벤치마크 놀이로 흐르지 않게 correctness-before-timing 원칙을 코드와 docs 모두에 남겨야 한다고 봤다. 그런데 실제로 글의 중심이 된 조치는 mutex, semaphore, condvar를 시나리오별로 배치하고, 출력 메트릭은 correctness를 통과한 뒤에만 의미가 있도록 정리했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/contention_lab.c`, `docs/concepts/correctness-before-timing.md`
- CLI: `make test && make run-demo`
- 검증 신호: docs concept와 시나리오 함수가 같은 전환점을 공유한다.

### 이 장면을 고정하는 코드 — `print_metrics` (`c/src/contention_lab.c:309`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

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

`print_metrics`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 동기화 primitive는 성능 옵션이 아니라 shared state invariant를 표현하는 문법이라는 점이 분명해졌다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 shell test와 demo scenario로 전 과정을 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 동기화 primitive는 성능 옵션이 아니라 shared state invariant를 표현하는 문법이라는 점이 분명해졌다.

그래서 다음 장면에서는 shell test와 demo scenario로 전 과정을 닫는다.

## Phase 3. self-owned shell test와 demo binary로 검증을 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 동기화 실험은 재현 가능한 시나리오 출력이 있어야 reasoning이 추상으로 남지 않는다.

처음에는 shell harness와 demo binary를 같이 남기면 primitive별 차이를 다시 확인하기 쉬울 것이라고 판단했다. 그런데 실제로 글의 중심이 된 조치는 `test_cases.sh`와 `problem/make run-demo`를 통해 counter/gate/buffer 결과를 반복 실행 가능하게 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/tests/test_cases.sh`, `c/src/main.c`
- CLI: `make test && make run-demo`
- 검증 신호: shell test와 demo 출력이 마지막 검증 신호를 남긴다.

### 이 장면을 고정하는 코드 — `main` (`c/src/main.c:11`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```c
int main(int argc, char **argv) {
    const char *scenario = NULL;
    int threads = 0;
    int iterations = 0;
```

`main`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 os 내부 주제도 작은 demo surface가 있으면 개념 note와 코드가 같은 문서 안에서 연결된다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 scenario design -> invariant choice -> demo verification 순서로 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 OS 내부 주제도 작은 demo surface가 있으면 개념 note와 코드가 같은 문서 안에서 연결된다.

그래서 다음 장면에서는 scenario design -> invariant choice -> demo verification 순서로 닫는다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

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

## 이번에 남은 질문

- 개념 축: `correctness before timing`, `mutex semaphore condvar`, `scenario invariants`
- 대표 테스트/fixture: `c/tests/test_cases.sh`
- 다음 질문: 최종 글은 scenario design -> invariant choice -> demo verification 순서로 닫는다.
