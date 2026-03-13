# Bomb Lab Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Bomb Lab에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `make clean && make test`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 입력 파서와 초기 phase를 먼저 고정한다 -> Phase 2 재귀와 자료구조가 숨어 있는 phase를 해석 절차로 바꾼다 -> Phase 3 정답 덤프 대신 self-owned mini bomb 검증으로 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - 입력 파서와 초기 phase를 먼저 고정한다

이 구간의 중심 장면은 폭탄의 핵심은 정답 문자열이 아니라, 문자열을 어떤 형식으로 읽고 비교하는지 해석하는 일이다.

본문에서는 먼저 초반 phase를 읽을 때 입력 형식을 잘못 잡으면 뒤 phase 전체가 흔들릴 거라고 봤다. 그 다음 문단에서는 `parse_*` helper와 `bomb_phase_1`~`bomb_phase_3`를 먼저 세워 phase별 입력 규칙을 코드로 재현했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `parse_six_ints`, `func4`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: 초기 phase들이 helper로 분리돼 있어 뒤 단계의 해석도 같은 표면으로 이어진다.
- 장면이 끝날 때 남길 문장: `func4`, linked-list phase, secret phase처럼 구조가 숨어 있는 구간으로 이동한다.

## 2. Phase 2 - 재귀와 자료구조가 숨어 있는 phase를 해석 절차로 바꾼다

이 구간의 중심 장면은 `func4`, `reset_nodes`, `fun7`는 단순 문자열 비교가 아니라 실행 구조를 읽어야 하는 구간이다.

본문에서는 먼저 bomb의 뒤쪽 phase는 조건식보다 호출 구조와 자료구조 invariant가 더 중요한 단서일 것이라고 예상했다. 그 다음 문단에서는 phase 4/6/secret phase를 helper 함수와 node reset 로직으로 풀어내면서 '무슨 값을 넣을까'보다 '왜 이 구조가 필요한가'를 코드로 남겼다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `func4`, `Func4`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: 자료구조 helper가 별도 함수로 남아 있어 판단 전환점을 코드에 연결할 수 있다.
- 장면이 끝날 때 남길 문장: sample answer와 unit test로 publication boundary를 넘지 않는지 점검한다.

## 3. Phase 3 - 정답 덤프 대신 self-owned mini bomb 검증으로 닫는다

이 구간의 중심 장면은 publication boundary를 지키려면 raw answer를 늘리는 대신 mini companion과 test가 reasoning을 대신 설명해야 한다.

본문에서는 먼저 sample answer 파일과 unit test만 있어도 phase별 계약을 재검증할 수 있을 것이라고 판단했다. 그 다음 문단에서는 `test_mini_bomb.c`와 sample run을 남기고, README에서는 공개 가능한 입력/검증 경로만 유지했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `secret accepts bst path`, `bomb_secret_phase`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: 실행 가능한 companion bomb가 남아 있어 마지막 단계가 추상 요약으로 끝나지 않는다.
- 장면이 끝날 때 남길 문장: 정답 목록이 아니라 해석 절차와 공개 경계 설계 기록으로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Foundations-CSAPP/bomblab/c && make clean && make test)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
