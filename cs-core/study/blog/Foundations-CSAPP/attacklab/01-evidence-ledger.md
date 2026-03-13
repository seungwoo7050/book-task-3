# Attack Lab Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`attacklab`은 stack layout, code injection, ROP, 상대 주소 계산을 단계적으로 익히는 프로젝트다. 구현의 중심은 `c`, `cpp`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `c/src/main.c`, `c/src/mini_attacklab.c`, `cpp/src/main.cpp`, `cpp/src/mini_attacklab.cpp`다. 검증 표면은 `c/tests/test_mini_attacklab.c`, `cpp/tests/test_mini_attacklab.cpp`와 `make clean && make test`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `payload models`, `rop and relative addressing`이다.

## Git History Anchor

- `2026-03-09	b1cbad9	docs(notion): cs-core, network-atda`
- `2026-03-10	ced9d08	docs: enhance cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - payload를 읽는 표면을 먼저 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 attacklab은 phase 정답보다 payload 바이트열을 어떤 형식으로 해석하는지가 먼저다.

그때 세운 가설은 hex parsing이 흔들리면 뒤 phase의 injection/ROP reasoning도 전부 불안정해질 거라고 봤다. 실제 조치는 `hex_value`, `parse_hex_string`, `load_hex_file`을 먼저 세워 입력 표면을 deterministic하게 만들었다.

- 정리해 둔 근거:
- 변경 단위: `c/src/mini_attacklab.c`
- CLI: `make clean && make test`
- 검증 신호: payload 로더가 따로 남아 있어 phase별 logic과 입력 해석을 혼동하지 않게 됐다.
- 새로 배운 것: 보안 lab에서도 가장 먼저 필요한 것은 exploit 자체보다 재현 가능한 input model이었다.

### 코드 앵커 — `hex_value` (`c/src/mini_attacklab.c:26`)

```c
static int hex_value(int ch)
{
    if ('0' <= ch && ch <= '9') {
        return ch - '0';
    }
    if ('a' <= ch && ch <= 'f') {
        return ch - 'a' + 10;
    }
    if ('A' <= ch && ch <= 'F') {
        return ch - 'A' + 10;
    }
    return -1;
```

이 조각은 payload 로더가 따로 남아 있어 phase별 logic과 입력 해석을 혼동하지 않게 됐다는 설명이 실제로 어디서 나오는지 보여 준다. `hex_value`를 읽고 나면 다음 장면이 왜 phase 1~5 validator로 넘어가면서 공격 기법 차이를 코드로 분리한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `parse_hex_string` (`c/src/mini_attacklab.c:56`)

```c
int parse_hex_string(const char *text, unsigned char *buffer, size_t capacity, size_t *out_len)
{
    size_t index = 0;

    while (*text != '\0') {
        while (isspace((unsigned char)*text)) {
            ++text;
        }
        if (*text == '#') {
            while (*text != '\0' && *text != '\n') {
                ++text;
            }
```

이 조각은 payload 로더가 따로 남아 있어 phase별 logic과 입력 해석을 혼동하지 않게 됐다는 설명이 실제로 어디서 나오는지 보여 준다. `parse_hex_string`를 읽고 나면 다음 장면이 왜 phase 1~5 validator로 넘어가면서 공격 기법 차이를 코드로 분리한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 phase 1~5 validator로 넘어가면서 공격 기법 차이를 코드로 분리한다.

## 2. Phase 2 - phase validator를 공격 기법별 contract로 바꾼다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 `attacklab_phase_1`~`attacklab_phase_5`는 한 덩어리 exploit dump가 아니라 서로 다른 검증 contract다.

그때 세운 가설은 코드 주입과 ROP를 같은 방식으로 설명하면 차이가 흐려질 것이라서 phase별로 기대하는 바이트/주소 패턴을 분리했다. 실제 조치는 validator 함수와 `matches_u64_le`, `read_u64_le` 같은 helper를 엮어 phase별 reasoning을 코드에서 바로 읽히게 했다.

- 정리해 둔 근거:
- 변경 단위: `c/src/mini_attacklab.c`
- CLI: `make clean && make test`
- 검증 신호: phase validator 분리가 되어 있어 injection과 ROP의 차이를 글에서도 단계적으로 전개할 수 있다.
- 새로 배운 것: 보안 과제는 성공 여부보다 '무슨 패턴을 검증하는가'를 분해할 때 설명 가능성이 생겼다.

### 코드 앵커 — `read_u64_le` (`c/src/mini_attacklab.c:40`)

```c
static uint64_t read_u64_le(const unsigned char *bytes)
{
    uint64_t value = 0;
    int index;
```

이 조각은 phase validator 분리가 되어 있어 injection과 rop의 차이를 글에서도 단계적으로 전개할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `read_u64_le`를 읽고 나면 다음 장면이 왜 sample payload와 unit test로 boundary를 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `matches_u64_le` (`c/src/mini_attacklab.c:51`)

```c
static int matches_u64_le(const unsigned char *bytes, uint64_t expected)
{
    return read_u64_le(bytes) == expected;
}
```

이 조각은 phase validator 분리가 되어 있어 injection과 rop의 차이를 글에서도 단계적으로 전개할 수 있다는 설명이 실제로 어디서 나오는지 보여 준다. `matches_u64_le`를 읽고 나면 다음 장면이 왜 sample payload와 unit test로 boundary를 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 sample payload와 unit test로 boundary를 닫는다.

## 3. Phase 3 - publication boundary를 지키는 self-owned 검증 루프를 만든다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 raw exploit answer를 늘리는 대신 sample payload와 unit test로 '왜 통과하는지'를 설명해야 한다.

그때 세운 가설은 phase data file과 unit test만 있으면 공개 가능한 범위에서 reasoning을 재현할 수 있다고 판단했다. 실제 조치는 `make test` 경로에 sample run을 넣고, README에서는 official boundary와 public test를 분리해 놓았다.

- 정리해 둔 근거:
- 변경 단위: `c/tests/test_mini_attacklab.c`, `c/src/mini_attacklab.c`
- CLI: `make clean && make test`
- 검증 신호: 샘플 phase 데이터와 테스트 바이너리가 마지막 단계를 구체적으로 닫아 준다.
- 새로 배운 것: 보안 실험은 답을 덜 공개할수록 오히려 검증 루프를 더 정교하게 설계해야 했다.

### 코드 앵커 — `attacklab_validate_phase` (`c/src/mini_attacklab.c:191`)

```c
int attacklab_validate_phase(int phase, const unsigned char *bytes, size_t len)
{
    switch (phase) {
    case 1:
        return attacklab_phase_1(bytes, len);
    case 2:
        return attacklab_phase_2(bytes, len);
    case 3:
        return attacklab_phase_3(bytes, len);
    case 4:
        return attacklab_phase_4(bytes, len);
    case 5:
```

이 조각은 샘플 phase 데이터와 테스트 바이너리가 마지막 단계를 구체적으로 닫아 준다는 설명이 실제로 어디서 나오는지 보여 준다. `attacklab_validate_phase`를 읽고 나면 다음 장면이 왜 payload dump 대신 입력 표면, validator, boundary 설계의 순서로 마무리한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `C mini-attacklab tests passed` (`c/tests/test_mini_attacklab.c:83`)

```c
    puts("C mini-attacklab tests passed");
    return 0;
}
```

이 조각은 샘플 phase 데이터와 테스트 바이너리가 마지막 단계를 구체적으로 닫아 준다는 설명이 실제로 어디서 나오는지 보여 준다. `C mini-attacklab tests passed`를 읽고 나면 다음 장면이 왜 payload dump 대신 입력 표면, validator, boundary 설계의 순서로 마무리한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 payload dump 대신 입력 표면, validator, boundary 설계의 순서로 마무리한다.

## Latest CLI Excerpt

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/attacklab/c && make clean && make test)
```

```text
C mini-attacklab tests passed
Phase 1 accepted: return-address overwrite
Phase 2 accepted: code injection with cookie register setup
Phase 3 accepted: code injection with cookie string placement
Phase 4 accepted: ROP chain for touch2
Phase 5 accepted: ROP chain for touch3 with relative string addressing
./build/test_mini_attacklab
```
