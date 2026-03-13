# Filesystem Mini Lab Evidence Ledger

이 문서는 최종 글보다 한 단계 앞에 있는 근거 문서다. 기존 `blog/` 초안은 입력에서 제외했고, 지금 남아 있는 README, problem 설명, 구현 파일, 테스트, git history, 재실행한 CLI만으로 chronology를 다시 세웠다.

## 근거 묶음

`filesystem-mini-lab`은 root-only toy filesystem으로 inode allocation, block allocation, metadata journaling, recovery를 작은 JSON disk image 위에서 설명하는 실험이다. 구현의 중심은 `python`에 퍼져 있고, 글에서 반복해서 참조할 핵심 파일은 `python/src/os_mini_fs/__init__.py`, `python/src/os_mini_fs/__main__.py`, `python/src/os_mini_fs/cli.py`, `python/src/os_mini_fs/core.py`다. 검증 표면은 `python/tests/test_os_mini_fs.py`와 `make test && make run-demo`에 걸쳐 있으며, 이번에 다시 붙잡은 개념 축은 `inode and blocks`, `journaling recovery`, `transaction states`이다.

## Git History Anchor

- `2026-03-11	0cccd64	feat: add new project in cs-core`
- `2026-03-11	bbb6673	Track 1에 대한 전반적인 개선 완료`
- `2026-03-13	abeead6	docs: TRACK 1 에대한 blog/ 작업 1차 완료`

## 1. Phase 1 - toy disk image와 기본 파일 연산을 먼저 고정한다

처음 손에 잡히는 문제는 이 단계가 없으면 뒤의 설명 전체가 흐려진다는 점이었다. 이 시점의 목표는 filesystem 실험도 결국 먼저 필요한 것은 inode/block을 어떻게 표현할지에 대한 저장 모델이다.

그때 세운 가설은 `mkfs`, `create`, `write`, `cat`, `list_files`가 없으면 journaling을 붙여도 무엇을 복구하는지 설명할 수 없다고 봤다. 실제 조치는 JSON image 구조와 root-only namespace를 먼저 세우고, inode/block bitmap을 다루는 기본 경로를 구현했다.

- 정리해 둔 근거:
- 변경 단위: `python/src/os_mini_fs/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: 기본 read/write path가 먼저 고정돼 있어 recovery가 무엇을 되돌리는지 선명해진다.
- 새로 배운 것: filesystem 개념은 디스크 형식을 간소화해도 inode/block contract를 남기면 충분히 재현할 수 있었다.

### 코드 앵커 — `mkfs` (`python/src/os_mini_fs/core.py:21`)

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

이 조각은 기본 read/write path가 먼저 고정돼 있어 recovery가 무엇을 되돌리는지 선명해진다는 설명이 실제로 어디서 나오는지 보여 준다. `mkfs`를 읽고 나면 다음 장면이 왜 transaction state와 recovery로 넘어간다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `list_files` (`python/src/os_mini_fs/core.py:48`)

```python
    def list_files(self) -> list[dict[str, int | str]]:
        image = self._load()
        files: list[dict[str, int | str]] = []
        for name in sorted(image["root"]):
            inode_index = image["root"][name]
            inode = image["inodes"][inode_index]
            files.append({"name": name, "size": inode["size"], "blocks": len(inode["blocks"])})
        return files
```

이 조각은 기본 read/write path가 먼저 고정돼 있어 recovery가 무엇을 되돌리는지 선명해진다는 설명이 실제로 어디서 나오는지 보여 준다. `list_files`를 읽고 나면 다음 장면이 왜 transaction state와 recovery로 넘어간다로 이어지는지도 한 번에 보인다.

다음 단계에서는 transaction state와 recovery로 넘어간다.

## 2. Phase 2 - prepare/commit/apply/finalize를 명시적으로 분리한다

두 번째 국면에서는 구현이 실제로 어디서 갈라지는지 코드가 말해 주기 시작한다. 이 시점의 목표는 이 실험의 중심은 journaling이 '로그를 남긴다'는 말보다 transaction state 전이를 어떤 순서로 밟는가에 있다.

그때 세운 가설은 crash recovery를 설명하려면 `_begin_transaction`, `_commit_transaction`, `_apply_and_finalize`, `recover`가 각자 하나의 상태를 담당해야 한다고 판단했다. 실제 조치는 prepared/committed entry를 분기하고, crash stage에 따라 replay/discard가 갈리는 구조를 코드와 tests로 묶었다.

- 정리해 둔 근거:
- 변경 단위: `python/src/os_mini_fs/core.py`
- CLI: `make test && make run-demo`
- 검증 신호: transaction helper와 recovery 테스트가 판단 전환점을 가장 잘 보여 준다.
- 새로 배운 것: journaling은 자료구조가 아니라 상태 전이 규칙이며, recovery는 그 규칙을 다시 실행하는 절차라는 점이 분명해졌다.

### 코드 앵커 — `recover` (`python/src/os_mini_fs/core.py:111`)

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

이 조각은 transaction helper와 recovery 테스트가 판단 전환점을 가장 잘 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `recover`를 읽고 나면 다음 장면이 왜 CLI demo와 crash test로 경계를 닫는다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `_begin_transaction` (`python/src/os_mini_fs/core.py:127`)

```python
    def _begin_transaction(self, image: dict, kind: str, payload: dict) -> int:
        txid = image["next_txid"]
        image["next_txid"] += 1
        image["journal"].append({"txid": txid, "kind": kind, "state": "prepared", "payload": payload})
        self._save(image)
        return txid
```

이 조각은 transaction helper와 recovery 테스트가 판단 전환점을 가장 잘 보여 준다는 설명이 실제로 어디서 나오는지 보여 준다. `_begin_transaction`를 읽고 나면 다음 장면이 왜 CLI demo와 crash test로 경계를 닫는다로 이어지는지도 한 번에 보인다.

다음 단계에서는 CLI demo와 crash test로 경계를 닫는다.

## 3. Phase 3 - CLI와 crash injection으로 journaling contract를 닫는다

마지막 국면에서는 설명이 아니라 검증 루프가 프로젝트를 닫아야 했다. 이 시점의 목표는 filesystem은 내부 메서드만 통과해서는 부족하고, 이미지 파일을 다시 열고 복구하는 end-to-end 흐름이 남아 있어야 한다.

그때 세운 가설은 command-line surface와 crash test가 남아 있으면 recovery reasoning을 더 이상 문장으로만 설명하지 않아도 된다고 봤다. 실제 조치는 `os_mini_fs/cli.py`와 `test_os_mini_fs.py`를 함께 두어 mkfs/create/write/recover 순서를 재현하게 만들었다.

- 정리해 둔 근거:
- 변경 단위: `python/tests/test_os_mini_fs.py`, `python/src/os_mini_fs/cli.py`
- CLI: `make test && make run-demo`
- 검증 신호: pytest와 demo 출력이 마지막 검증 신호를 남긴다.
- 새로 배운 것: toy lab이라도 CLI가 있으면 데이터 구조, crash stage, recovery 결과가 한 줄로 연결된다.

### 코드 앵커 — `main` (`python/src/os_mini_fs/cli.py:37`)

```python
def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "mkfs":
        MiniFS.mkfs(args.image, args.inodes, args.blocks, args.block_size)
        print(f"mkfs image={args.image} inodes={args.inodes} blocks={args.blocks}")
        return 0
```

이 조각은 pytest와 demo 출력이 마지막 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `main`를 읽고 나면 다음 장면이 왜 disk image -> journal state -> CLI recovery 순서로 정리한다로 이어지는지도 한 번에 보인다.

### 코드 앵커 — `test_prepared_journal_is_discarded` (`python/tests/test_os_mini_fs.py:41`)

```python
def test_prepared_journal_is_discarded(tmp_path: Path) -> None:
    fs = make_fs(tmp_path)
    fs.create("note")
    fs.write("note", "old")
    try:
        fs.write("note", "newer", crash_stage="after_prepare")
    except SimulatedCrash:
        pass
    stats = fs.recover()
    assert stats["discarded"] == 1
    assert fs.cat("note") == "old"
```

이 조각은 pytest와 demo 출력이 마지막 검증 신호를 남긴다는 설명이 실제로 어디서 나오는지 보여 준다. `test_prepared_journal_is_discarded`를 읽고 나면 다음 장면이 왜 disk image -> journal state -> CLI recovery 순서로 정리한다로 이어지는지도 한 번에 보인다.

다음 단계에서는 disk image -> journal state -> CLI recovery 순서로 정리한다.

## Latest CLI Excerpt

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
