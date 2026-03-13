# Bomb Lab 재구성 개발 로그

`bomblab`은 x86-64 bomb를 brute force가 아니라 해석 절차로 풀어 가는 프로젝트다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

phase별 입력 조건을 brute force 대신 해석 절차로 옮기고, 그 해석이 테스트 가능한 mini bomb로 바뀌는 흐름을 복원한다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: 입력 파서와 초기 phase를 먼저 고정한다 — `c/src/mini_bomb.c`
- Phase 2: 재귀와 자료구조가 숨어 있는 phase를 해석 절차로 바꾼다 — `c/src/mini_bomb.c`
- Phase 3: 정답 덤프 대신 self-owned mini bomb 검증으로 닫는다 — `c/tests/test_mini_bomb.c`, `c/src/mini_bomb.c`

## Phase 1. 입력 파서와 초기 phase를 먼저 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 폭탄의 핵심은 정답 문자열이 아니라, 문자열을 어떤 형식으로 읽고 비교하는지 해석하는 일이다.

처음에는 초반 phase를 읽을 때 입력 형식을 잘못 잡으면 뒤 phase 전체가 흔들릴 거라고 봤다. 그런데 실제로 글의 중심이 된 조치는 `parse_*` helper와 `bomb_phase_1`~`bomb_phase_3`를 먼저 세워 phase별 입력 규칙을 코드로 재현했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/mini_bomb.c`
- CLI: `make clean && make test`
- 검증 신호: 초기 phase들이 helper로 분리돼 있어 뒤 단계의 해석도 같은 표면으로 이어진다.

### 이 장면을 고정하는 코드 — `parse_six_ints` (`c/src/mini_bomb.c:29`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

```c
static int parse_six_ints(const char *input, int values[6])
{
    char tail;

    return input != NULL &&
           sscanf(
               input,
               " %d %d %d %d %d %d %c",
               &values[0],
               &values[1],
               &values[2],
               &values[3],
```

`parse_six_ints`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 역공학 초기 단계는 정답을 맞히는 것보다 입력 surface를 정확히 복원하는 데 더 많은 시간을 써야 했다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 `func4`, linked-list phase, secret phase처럼 구조가 숨어 있는 구간으로 이동한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 역공학 초기 단계는 정답을 맞히는 것보다 입력 surface를 정확히 복원하는 데 더 많은 시간을 써야 했다.

그래서 다음 장면에서는 `func4`, linked-list phase, secret phase처럼 구조가 숨어 있는 구간으로 이동한다.

## Phase 2. 재귀와 자료구조가 숨어 있는 phase를 해석 절차로 바꾼다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 `func4`, `reset_nodes`, `fun7`는 단순 문자열 비교가 아니라 실행 구조를 읽어야 하는 구간이다.

처음에는 bomb의 뒤쪽 phase는 조건식보다 호출 구조와 자료구조 invariant가 더 중요한 단서일 것이라고 예상했다. 그런데 실제로 글의 중심이 된 조치는 phase 4/6/secret phase를 helper 함수와 node reset 로직으로 풀어내면서 '무슨 값을 넣을까'보다 '왜 이 구조가 필요한가'를 코드로 남겼다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/mini_bomb.c`
- CLI: `make clean && make test`
- 검증 신호: 자료구조 helper가 별도 함수로 남아 있어 판단 전환점을 코드에 연결할 수 있다.

### 이 장면을 고정하는 코드 — `func4` (`c/src/mini_bomb.c:70`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

```c
static int func4(int target, int low, int high)
{
    int mid = low + (high - low) / 2;

    if (mid == target) {
        return 0;
    }
    if (target < mid) {
        return 2 * func4(target, low, mid - 1);
    }
    return 2 * func4(target, mid + 1, high) + 1;
}
```

`func4`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 재귀/리스트/트리 phase는 정답을 외우기보다 실행 경로를 복원했을 때만 재사용 가능한 설명이 된다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 sample answer와 unit test로 publication boundary를 넘지 않는지 점검한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 재귀/리스트/트리 phase는 정답을 외우기보다 실행 경로를 복원했을 때만 재사용 가능한 설명이 된다.

그래서 다음 장면에서는 sample answer와 unit test로 publication boundary를 넘지 않는지 점검한다.

## Phase 3. 정답 덤프 대신 self-owned mini bomb 검증으로 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 publication boundary를 지키려면 raw answer를 늘리는 대신 mini companion과 test가 reasoning을 대신 설명해야 한다.

처음에는 sample answer 파일과 unit test만 있어도 phase별 계약을 재검증할 수 있을 것이라고 판단했다. 그런데 실제로 글의 중심이 된 조치는 `test_mini_bomb.c`와 sample run을 남기고, README에서는 공개 가능한 입력/검증 경로만 유지했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/tests/test_mini_bomb.c`, `c/src/mini_bomb.c`
- CLI: `make clean && make test`
- 검증 신호: 실행 가능한 companion bomb가 남아 있어 마지막 단계가 추상 요약으로 끝나지 않는다.

### 이 장면을 고정하는 코드 — `secret accepts bst path` (`c/tests/test_mini_bomb.c:50`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```c
    expect_true("secret accepts bst path", bomb_secret_phase("35"));
    expect_false("secret rejects another node", bomb_secret_phase("99"));
    expect_false("secret rejects non-number", bomb_secret_phase("thirty-five"));

    if (failures != 0) {
        return 1;
    }
```

`secret accepts bst path`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 reverse engineering 프로젝트일수록 '무엇을 공개하지 않을지'를 검증 경로 안에 같이 설계해야 했다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 정답 목록이 아니라 해석 절차와 공개 경계 설계 기록으로 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 reverse engineering 프로젝트일수록 '무엇을 공개하지 않을지'를 검증 경로 안에 같이 설계해야 했다.

그래서 다음 장면에서는 정답 목록이 아니라 해석 절차와 공개 경계 설계 기록으로 닫는다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/bomblab/c && make clean && make test)
```

```text
C mini-bomb tests passed
./build/test_mini_bomb
```

## 이번에 남은 질문

- 개념 축: `phase patterns`, `reverse engineering workflow`
- 대표 테스트/fixture: `c/tests/test_mini_bomb.c`, `cpp/tests/test_mini_bomb.cpp`
- 다음 질문: 최종 글은 정답 목록이 아니라 해석 절차와 공개 경계 설계 기록으로 닫는다.
