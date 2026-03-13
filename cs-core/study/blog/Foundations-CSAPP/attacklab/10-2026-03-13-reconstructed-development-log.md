# Attack Lab 재구성 개발 로그

`attacklab`은 stack layout, code injection, ROP, 상대 주소 계산을 단계적으로 익히는 프로젝트다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

hex payload를 읽는 표면부터 phase validator까지 이어 붙여, code injection/ROP를 raw exploit dump가 아닌 재현 가능한 companion lab로 재구성한 흐름을 다룬다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: payload를 읽는 표면을 먼저 고정한다 — `c/src/mini_attacklab.c`
- Phase 2: phase validator를 공격 기법별 contract로 바꾼다 — `c/src/mini_attacklab.c`
- Phase 3: publication boundary를 지키는 self-owned 검증 루프를 만든다 — `c/tests/test_mini_attacklab.c`, `c/src/mini_attacklab.c`

## Phase 1. payload를 읽는 표면을 먼저 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 attacklab은 phase 정답보다 payload 바이트열을 어떤 형식으로 해석하는지가 먼저다.

처음에는 hex parsing이 흔들리면 뒤 phase의 injection/ROP reasoning도 전부 불안정해질 거라고 봤다. 그런데 실제로 글의 중심이 된 조치는 `hex_value`, `parse_hex_string`, `load_hex_file`을 먼저 세워 입력 표면을 deterministic하게 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/mini_attacklab.c`
- CLI: `make clean && make test`
- 검증 신호: payload 로더가 따로 남아 있어 phase별 logic과 입력 해석을 혼동하지 않게 됐다.

### 이 장면을 고정하는 코드 — `hex_value` (`c/src/mini_attacklab.c:26`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

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

`hex_value`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 보안 lab에서도 가장 먼저 필요한 것은 exploit 자체보다 재현 가능한 input model이었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 phase 1~5 validator로 넘어가면서 공격 기법 차이를 코드로 분리한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 보안 lab에서도 가장 먼저 필요한 것은 exploit 자체보다 재현 가능한 input model이었다.

그래서 다음 장면에서는 phase 1~5 validator로 넘어가면서 공격 기법 차이를 코드로 분리한다.

## Phase 2. phase validator를 공격 기법별 contract로 바꾼다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 `attacklab_phase_1`~`attacklab_phase_5`는 한 덩어리 exploit dump가 아니라 서로 다른 검증 contract다.

처음에는 코드 주입과 ROP를 같은 방식으로 설명하면 차이가 흐려질 것이라서 phase별로 기대하는 바이트/주소 패턴을 분리했다. 그런데 실제로 글의 중심이 된 조치는 validator 함수와 `matches_u64_le`, `read_u64_le` 같은 helper를 엮어 phase별 reasoning을 코드에서 바로 읽히게 했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/src/mini_attacklab.c`
- CLI: `make clean && make test`
- 검증 신호: phase validator 분리가 되어 있어 injection과 ROP의 차이를 글에서도 단계적으로 전개할 수 있다.

### 이 장면을 고정하는 코드 — `read_u64_le` (`c/src/mini_attacklab.c:40`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

```c
static uint64_t read_u64_le(const unsigned char *bytes)
{
    uint64_t value = 0;
    int index;
```

`read_u64_le`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 보안 과제는 성공 여부보다 '무슨 패턴을 검증하는가'를 분해할 때 설명 가능성이 생겼다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 sample payload와 unit test로 boundary를 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 보안 과제는 성공 여부보다 '무슨 패턴을 검증하는가'를 분해할 때 설명 가능성이 생겼다.

그래서 다음 장면에서는 sample payload와 unit test로 boundary를 닫는다.

## Phase 3. publication boundary를 지키는 self-owned 검증 루프를 만든다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 raw exploit answer를 늘리는 대신 sample payload와 unit test로 '왜 통과하는지'를 설명해야 한다.

처음에는 phase data file과 unit test만 있으면 공개 가능한 범위에서 reasoning을 재현할 수 있다고 판단했다. 그런데 실제로 글의 중심이 된 조치는 `make test` 경로에 sample run을 넣고, README에서는 official boundary와 public test를 분리해 놓았다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `c/tests/test_mini_attacklab.c`, `c/src/mini_attacklab.c`
- CLI: `make clean && make test`
- 검증 신호: 샘플 phase 데이터와 테스트 바이너리가 마지막 단계를 구체적으로 닫아 준다.

### 이 장면을 고정하는 코드 — `attacklab_validate_phase` (`c/src/mini_attacklab.c:191`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

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

`attacklab_validate_phase`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 보안 실험은 답을 덜 공개할수록 오히려 검증 루프를 더 정교하게 설계해야 했다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 payload dump 대신 입력 표면, validator, boundary 설계의 순서로 마무리한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 보안 실험은 답을 덜 공개할수록 오히려 검증 루프를 더 정교하게 설계해야 했다.

그래서 다음 장면에서는 payload dump 대신 입력 표면, validator, boundary 설계의 순서로 마무리한다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

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

## 이번에 남은 질문

- 개념 축: `payload models`, `rop and relative addressing`
- 대표 테스트/fixture: `c/tests/test_mini_attacklab.c`, `cpp/tests/test_mini_attacklab.cpp`
- 다음 질문: 최종 글은 payload dump 대신 입력 표면, validator, boundary 설계의 순서로 마무리한다.
