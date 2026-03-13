# Bomb Lab Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`bomblab`은 x86-64 bomb를 brute force가 아니라 해석 절차로 풀어 가는 프로젝트다. 구현의 중심은 `c`, `cpp`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `c/src/main.c`, `c/src/mini_bomb.c`, `cpp/src/main.cpp`, `cpp/src/mini_bomb.cpp`다. 검증 표면은 `c/tests/test_mini_bomb.c`, `cpp/tests/test_mini_bomb.cpp`와 `make clean && make test`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `phase patterns`, `reverse engineering workflow`이다.

## Git History Anchor

- `2026-03-09	b1cbad9	docs(notion): cs-core, network-atda`
- `2026-03-10	ced9d08	docs: enhance cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - 입력 파서와 초기 phase를 먼저 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 폭탄의 핵심은 정답 문자열이 아니라, 문자열을 어떤 형식으로 읽고 비교하는지 해석하는 일이다.

그때 세운 가설은 초반 phase를 읽을 때 입력 형식을 잘못 잡으면 뒤 phase 전체가 흔들릴 거라고 봤다. 실제 조치는 `parse_*` helper와 `bomb_phase_1`~`bomb_phase_3`를 먼저 세워 phase별 입력 규칙을 코드로 재현했다.

- 정리해 둔 근거:
- 변경 단위: `c/src/mini_bomb.c`
- CLI: `make clean && make test`
- 검증 신호: 초기 phase들이 helper로 분리돼 있어 뒤 단계의 해석도 같은 표면으로 이어진다.
- 새로 배운 것: 역공학 초기 단계는 정답을 맞히는 것보다 입력 surface를 정확히 복원하는 데 더 많은 시간을 써야 했다.

### 코드 앵커 — `parse_six_ints` (`c/src/mini_bomb.c:29`)

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

이 조각은 초기 phase들이 helper로 분리돼 있어 뒤 단계의 해석도 같은 표면으로 이어진다는 설명이 실제로 어디서 나오는지 보여 준다. `parse_six_ints`를 읽고 나면 다음 장면이 왜 `func4`, linked-list phase, secret phase처럼 구조가 숨어 있는 구간으로 이동한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `func4` (`c/src/mini_bomb.c:70`)

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

이 조각은 초기 phase들이 helper로 분리돼 있어 뒤 단계의 해석도 같은 표면으로 이어진다는 설명이 실제로 어디서 나오는지 보여 준다. `func4`를 읽고 나면 다음 장면이 왜 `func4`, linked-list phase, secret phase처럼 구조가 숨어 있는 구간으로 이동한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 `func4`, linked-list phase, secret phase처럼 구조가 숨어 있는 구간으로 이동한다.

## 2. Phase 2 - 재귀와 자료구조가 숨어 있는 phase를 해석 절차로 바꾼다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `func4`, `reset_nodes`, `fun7`는 단순 문자열 비교가 아니라 실행 구조를 읽어야 하는 구간이다.

그때 세운 가설은 bomb의 뒤쪽 phase는 조건식보다 호출 구조와 자료구조 invariant가 더 중요한 단서일 것이라고 예상했다. 실제 조치는 phase 4/6/secret phase를 helper 함수와 node reset 로직으로 풀어내면서 '무슨 값을 넣을까'보다 '왜 이 구조가 필요한가'를 코드로 남겼다.

- 정리해 둔 근거:
- 변경 단위: `c/src/mini_bomb.c`
- CLI: `make clean && make test`
- 검증 신호: 자료구조 helper가 별도 함수로 남아 있어 판단 전환점을 코드에 연결할 수 있다.
- 새로 배운 것: 재귀/리스트/트리 phase는 정답을 외우기보다 실행 경로를 복원했을 때만 재사용 가능한 설명이 된다.

### 코드 앵커 — `func4` (`c/src/mini_bomb.c:70`)

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

이 조각은 자료구조 helper가 별도 함수로 남아 있어 판단 전환점을 코드에 연결할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `func4`를 읽고 나면 다음 장면이 왜 sample answer와 unit test로 publication boundary를 넘지 않는지 점검한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `func4` (`c/src/mini_bomb.c:70`)

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

이 조각은 자료구조 helper가 별도 함수로 남아 있어 판단 전환점을 코드에 연결할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `Func4`를 읽고 나면 다음 장면이 왜 sample answer와 unit test로 publication boundary를 넘지 않는지 점검한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 sample answer와 unit test로 publication boundary를 넘지 않는지 점검한다.

## 3. Phase 3 - 정답 덤프 대신 self-owned mini bomb 검증으로 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 publication boundary를 지키려면 raw answer를 늘리는 대신 mini companion과 test가 reasoning을 대신 설명해야 한다.

그때 세운 가설은 sample answer 파일과 unit test만 있어도 phase별 계약을 재검증할 수 있을 것이라고 판단했다. 실제 조치는 `test_mini_bomb.c`와 sample run을 남기고, README에서는 공개 가능한 입력/검증 경로만 유지했다.

- 정리해 둔 근거:
- 변경 단위: `c/tests/test_mini_bomb.c`, `c/src/mini_bomb.c`
- CLI: `make clean && make test`
- 검증 신호: 실행 가능한 companion bomb가 남아 있어 마지막 단계가 추상 요약으로 끝나지 않는다.
- 새로 배운 것: reverse engineering 프로젝트일수록 '무엇을 공개하지 않을지'를 검증 경로 안에 같이 설계해야 했다.

### 코드 앵커 — `secret accepts bst path` (`c/tests/test_mini_bomb.c:50`)

```c
    expect_true("secret accepts bst path", bomb_secret_phase("35"));
    expect_false("secret rejects another node", bomb_secret_phase("99"));
    expect_false("secret rejects non-number", bomb_secret_phase("thirty-five"));

    if (failures != 0) {
        return 1;
    }
```

이 조각은 실행 가능한 companion bomb가 남아 있어 마지막 단계가 추상 요약으로 끝나지 않는다는 설명이 실제로 어디서 나오는지 보여 준다. `secret accepts bst path`를 읽고 나면 다음 장면이 왜 정답 목록이 아니라 해석 절차와 공개 경계 설계 기록으로 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `bomb_secret_phase` (`c/src/mini_bomb.c:218`)

```c
int bomb_secret_phase(const char *input)
{
    TreeNode n6 = {6, NULL, NULL};
    TreeNode n20 = {20, NULL, NULL};
    TreeNode n35 = {35, NULL, NULL};
    TreeNode n45 = {45, NULL, NULL};
    TreeNode n99 = {99, NULL, NULL};
    TreeNode n1001 = {1001, NULL, NULL};
    TreeNode n22 = {22, &n20, &n35};
    TreeNode n107 = {107, &n99, &n1001};
    TreeNode n8 = {8, &n6, &n22};
    TreeNode n50 = {50, &n45, &n107};
```

이 조각은 실행 가능한 companion bomb가 남아 있어 마지막 단계가 추상 요약으로 끝나지 않는다는 설명이 실제로 어디서 나오는지 보여 준다. `bomb_secret_phase`를 읽고 나면 다음 장면이 왜 정답 목록이 아니라 해석 절차와 공개 경계 설계 기록으로 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 정답 목록이 아니라 해석 절차와 공개 경계 설계 기록으로 닫는다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/bomblab/c && make clean && make test)
```

```text
C mini-bomb tests passed
./build/test_mini_bomb
```
