# Filesystem Mini Lab Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Filesystem Mini Lab에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `make test && make run-demo`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 toy disk image와 기본 파일 연산을 먼저 고정한다 -> Phase 2 prepare/commit/apply/finalize를 명시적으로 분리한다 -> Phase 3 CLI와 crash injection으로 journaling contract를 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - toy disk image와 기본 파일 연산을 먼저 고정한다

이 구간의 중심 장면은 filesystem 실험도 결국 먼저 필요한 것은 inode/block을 어떻게 표현할지에 대한 저장 모델이다.

본문에서는 먼저 `mkfs`, `create`, `write`, `cat`, `list_files`가 없으면 journaling을 붙여도 무엇을 복구하는지 설명할 수 없다고 봤다. 그 다음 문단에서는 JSON image 구조와 root-only namespace를 먼저 세우고, inode/block bitmap을 다루는 기본 경로를 구현했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `mkfs`, `list_files`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: 기본 read/write path가 먼저 고정돼 있어 recovery가 무엇을 되돌리는지 선명해진다.
- 장면이 끝날 때 남길 문장: transaction state와 recovery로 넘어간다.

## 2. Phase 2 - prepare/commit/apply/finalize를 명시적으로 분리한다

이 구간의 중심 장면은 이 실험의 중심은 journaling이 '로그를 남긴다'는 말보다 transaction state 전이를 어떤 순서로 밟는가에 있다.

본문에서는 먼저 crash recovery를 설명하려면 `_begin_transaction`, `_commit_transaction`, `_apply_and_finalize`, `recover`가 각자 하나의 상태를 담당해야 한다고 판단했다. 그 다음 문단에서는 prepared/committed entry를 분기하고, crash stage에 따라 replay/discard가 갈리는 구조를 코드와 tests로 묶었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `recover`, `_begin_transaction`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: transaction helper와 recovery 테스트가 판단 전환점을 가장 잘 보여 준다.
- 장면이 끝날 때 남길 문장: CLI demo와 crash test로 경계를 닫는다.

## 3. Phase 3 - CLI와 crash injection으로 journaling contract를 닫는다

이 구간의 중심 장면은 filesystem은 내부 메서드만 통과해서는 부족하고, 이미지 파일을 다시 열고 복구하는 end-to-end 흐름이 남아 있어야 한다.

본문에서는 먼저 command-line surface와 crash test가 남아 있으면 recovery reasoning을 더 이상 문장으로만 설명하지 않아도 된다고 봤다. 그 다음 문단에서는 `os_mini_fs/cli.py`와 `test_os_mini_fs.py`를 함께 두어 mkfs/create/write/recover 순서를 재현하게 만들었다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `main`, `test_prepared_journal_is_discarded`
- 붙일 CLI: `make test && make run-demo`
- 강조할 검증 신호: pytest와 demo 출력이 마지막 검증 신호를 남긴다.
- 장면이 끝날 때 남길 문장: disk image -> journal state -> CLI recovery 순서로 정리한다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/filesystem-mini-lab/problem && make test && make run-demo)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
