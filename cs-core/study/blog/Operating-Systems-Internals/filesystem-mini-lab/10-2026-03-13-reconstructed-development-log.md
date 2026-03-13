# Filesystem Mini Lab 재구성 개발 로그

`filesystem-mini-lab`은 root-only toy filesystem으로 inode allocation, block allocation, metadata journaling, recovery를 작은 JSON disk image 위에서 설명하는 실험이다.

2026-03-13에 기존 초안을 `_legacy`로 격리한 뒤, `README`, `problem/`, 실제 구현 파일, `docs/`, 테스트, 현재 다시 실행한 CLI만으로 이 글을 다시 썼다. 그래서 아래 서사는 나중에 답을 알고 난 뒤 매끈하게 정리한 회고가 아니라, 남아 있는 증거를 따라 다시 세운 개발 흐름에 가깝다.

## 이 프로젝트를 다시 읽는 순서

inode/block allocator를 먼저 세운 뒤 journal prepare/commit/apply/recover가 왜 별도 단계여야 하는지 따라간다. 이 질문이 너무 빨리 추상적으로 흘러가지 않도록, 글은 세 개의 phase로 나눠 진행한다.

- Phase 1: toy disk image와 기본 파일 연산을 먼저 고정한다 — `python/src/os_mini_fs/core.py`
- Phase 2: prepare/commit/apply/finalize를 명시적으로 분리한다 — `python/src/os_mini_fs/core.py`
- Phase 3: CLI와 crash injection으로 journaling contract를 닫는다 — `python/tests/test_os_mini_fs.py`, `python/src/os_mini_fs/cli.py`

## Phase 1. toy disk image와 기본 파일 연산을 먼저 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다.

이 시점의 목표는 filesystem 실험도 결국 먼저 필요한 것은 inode/block을 어떻게 표현할지에 대한 저장 모델이다.

처음에는 `mkfs`, `create`, `write`, `cat`, `list_files`가 없으면 journaling을 붙여도 무엇을 복구하는지 설명할 수 없다고 봤다. 그런데 실제로 글의 중심이 된 조치는 JSON image 구조와 root-only namespace를 먼저 세우고, inode/block bitmap을 다루는 기본 경로를 구현했다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `python/src/os_mini_fs/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: 기본 read/write path가 먼저 고정돼 있어 recovery가 무엇을 되돌리는지 선명해진다.

### 이 장면을 고정하는 코드 — `mkfs` (`python/src/os_mini_fs/core.py:21`)

이 단계에서 가장 먼저 붙잡아야 하는 코드는 아래 조각이다.

```python
    def mkfs(
        cls,
        image_path: str | Path,
        inode_count: int,
        block_count: int,
        block_size: int = 16,
    ) -> "MiniFS":
        image = {
            "superblock": {
                "inode_count": inode_count,
                "block_count": block_count,
                "block_size": block_size,
```

`mkfs`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 filesystem 개념은 디스크 형식을 간소화해도 inode/block contract를 남기면 충분히 재현할 수 있었다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 transaction state와 recovery로 넘어간다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 filesystem 개념은 디스크 형식을 간소화해도 inode/block contract를 남기면 충분히 재현할 수 있었다.

그래서 다음 장면에서는 transaction state와 recovery로 넘어간다.

## Phase 2. prepare/commit/apply/finalize를 명시적으로 분리한다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다.

이 시점의 목표는 이 실험의 중심은 journaling이 '로그를 남긴다'는 말보다 transaction state 전이를 어떤 순서로 밟는가에 있다.

처음에는 crash recovery를 설명하려면 `_begin_transaction`, `_commit_transaction`, `_apply_and_finalize`, `recover`가 각자 하나의 상태를 담당해야 한다고 판단했다. 그런데 실제로 글의 중심이 된 조치는 prepared/committed entry를 분기하고, crash stage에 따라 replay/discard가 갈리는 구조를 코드와 tests로 묶었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `python/src/os_mini_fs/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: transaction helper와 recovery 테스트가 판단 전환점을 가장 잘 보여 준다.

### 이 장면을 고정하는 코드 — `recover` (`python/src/os_mini_fs/core.py:111`)

판단이 뒤집히는 지점은 결국 이 구현 세부에서 드러난다.

```python
    def recover(self) -> dict[str, int]:
        image = self._load()
        replayed = 0
        discarded = 0
        for entry in list(image["journal"]):
            if entry["state"] == "prepared":
                discarded += 1
                self._discard_prepared(image, entry)
                image["journal"].remove(entry)
                continue
            replayed += 1
            self._apply_entry(image, entry)
```

`recover`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 journaling은 자료구조가 아니라 상태 전이 규칙이며, recovery는 그 규칙을 다시 실행하는 절차라는 점이 분명해졌다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 CLI demo와 crash test로 경계를 닫는다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 journaling은 자료구조가 아니라 상태 전이 규칙이며, recovery는 그 규칙을 다시 실행하는 절차라는 점이 분명해졌다.

그래서 다음 장면에서는 CLI demo와 crash test로 경계를 닫는다.

## Phase 3. CLI와 crash injection으로 journaling contract를 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다.

이 시점의 목표는 filesystem은 내부 메서드만 통과해서는 부족하고, 이미지 파일을 다시 열고 복구하는 end-to-end 흐름이 남아 있어야 한다.

처음에는 command-line surface와 crash test가 남아 있으면 recovery reasoning을 더 이상 문장으로만 설명하지 않아도 된다고 봤다. 그런데 실제로 글의 중심이 된 조치는 `os_mini_fs/cli.py`와 `test_os_mini_fs.py`를 함께 두어 mkfs/create/write/recover 순서를 재현하게 만들었다. 그래서 이 단계는 결론을 단번에 얻는 장면이 아니라, 문제를 어디까지 좁힐 수 있는지 확인하는 장면으로 읽는 편이 자연스럽다.

- 변경 단위: `python/tests/test_os_mini_fs.py`, `python/src/os_mini_fs/cli.py`
- CLI: `make test && make run-demo`
- 검증 신호: pytest와 demo 출력이 마지막 검증 신호를 남긴다.

### 이 장면을 고정하는 코드 — `main` (`python/src/os_mini_fs/cli.py:37`)

끝을 닫는 순간은 늘 테스트나 CLI 쪽 코드가 더 솔직하게 보여 준다.

```python
def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "mkfs":
        MiniFS.mkfs(args.image, args.inodes, args.blocks, args.block_size)
        print(f"mkfs image={args.image} inodes={args.inodes} blocks={args.blocks}")
        return 0
```

`main`는 이 phase를 추상 설명에서 실제 구현으로 끌어내린다. 이 코드를 읽고 나면 toy lab이라도 cli가 있으면 데이터 구조, crash stage, recovery 결과가 한 줄로 연결된다는 설명이 어디서 나오는지 알 수 있고, 다음 장면에서 왜 disk image -> journal state -> CLI recovery 순서로 정리한다를 붙잡게 되는지도 보인다.

이 단계에서 새로 굳은 이해는 toy lab이라도 CLI가 있으면 데이터 구조, crash stage, recovery 결과가 한 줄로 연결된다.

그래서 다음 장면에서는 disk image -> journal state -> CLI recovery 순서로 정리한다.

## CLI로 다시 닫기

문장과 코드만으로는 마지막 닫힘이 약해질 수 있어서, 저장소에서 다시 실행 가능한 대표 명령을 마지막에 그대로 남긴다. 이 출력은 기능이 돌아간다는 사실뿐 아니라 README가 약속한 검증 entrypoint가 아직 살아 있다는 사실까지 함께 보여 준다.

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Operating-Systems-Internals/filesystem-mini-lab/problem && make test && make run-demo)
```

```text
used_inodes=2 used_blocks=1 journal_entries=0
[cat note]
hello-os
[simulated crash] simulated crash at after_commit
[after recover]
{'replayed': 1, 'discarded': 0}
files=note(11B/2blk)
used_inodes=2 used_blocks=2 journal_entries=0
```

## 이번에 남은 질문

- 개념 축: `inode and blocks`, `journaling recovery`, `transaction states`
- 대표 테스트/fixture: `python/tests/test_os_mini_fs.py`
- 다음 질문: 최종 글은 disk image -> journal state -> CLI recovery 순서로 정리한다.
