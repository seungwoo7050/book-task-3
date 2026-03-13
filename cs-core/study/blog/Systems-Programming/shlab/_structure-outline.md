# Shell Lab Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Shell Lab에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `make clean && make test`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 파서, builtin, job table부터 고정한다 -> Phase 2 `waitfg`와 signal handler에서 race discipline을 고정한다 -> Phase 3 trace와 direct shell case로 shell contract를 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - 파서, builtin, job table부터 고정한다

이 구간의 중심 장면은 tiny shell도 결국 먼저 필요한 것은 command surface와 job bookkeeping이다.

본문에서는 먼저 `eval`과 `parseline`이 흔들리면 foreground/background 구분조차 무의미해질 거라고 봤다. 그 다음 문단에서는 파서, builtin 분기, `addjob`/`clearjob` 같은 job table helper를 먼저 묶었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `Eval`, `builtin_cmd`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: job table helper가 남아 있어 signal reasoning을 뒤에서 덧붙일 수 있다.
- 장면이 끝날 때 남길 문장: foreground wait와 signal forwarding으로 이동한다.

## 2. Phase 2 - `waitfg`와 signal handler에서 race discipline을 고정한다

이 구간의 중심 장면은 `waitfg`, `sigchld_handler`, `sigint_handler`, `sigtstp_handler`는 shell의 실제 난점이 어디인지 드러내는 함수들이다.

본문에서는 먼저 문제의 중심은 명령 실행 자체가 아니라 `fork` 주변 마스킹 순서와 job state 전이일 것이라고 판단했다. 그 다음 문단에서는 signal handler와 foreground wait를 분리하고, docs에서 job control flow와 race discipline을 설명하는 구조로 정리했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `Waitfg`, `sigchld_handler`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: 핵심 race가 함수 수준으로 드러나 있어 블로그에서도 판단 전환점을 분명히 보여 줄 수 있다.
- 장면이 끝날 때 남길 문장: trace와 direct-shell case로 동작을 닫는다.

## 3. Phase 3 - trace와 direct shell case로 shell contract를 닫는다

이 구간의 중심 장면은 shell은 한두 개의 unit test보다 trace sequence가 더 많은 것을 말해 준다.

본문에서는 먼저 공식 trace 없이도 self-owned trace와 `direct_shell_case.sh`가 있으면 핵심 job-control contract를 재현할 수 있다고 봤다. 그 다음 문단에서는 `tests/`와 `c/tests/run_tests.sh`를 중심으로 foreground stop, bg jobs, SIGINT 시나리오를 다시 확인하게 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `$SHELL_PATH`, `C`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: 현재 테스트 출력이 마지막 단계의 닫힘을 명확히 보여 준다.
- 장면이 끝날 때 남길 문장: shell surface -> race discipline -> trace verification 순서를 유지한다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/shlab/c && make clean && make test)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
