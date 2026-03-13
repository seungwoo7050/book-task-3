# 20 01 Mini LSM Store의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `SSTable`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/01-mini-lsm-store/src/mini_lsm_store/store.py`의 `SSTable`
- 처음 가설:
  `SSTable` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "SSTable|MiniLSMStore" src`로 핵심 함수 위치를 다시 잡고, `SSTable`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "SSTable|MiniLSMStore" src
src/mini_lsm_store/__init__.py:1:from .store import MiniLSMStore, SSTable
src/mini_lsm_store/__init__.py:3:__all__ = ["MiniLSMStore", "SSTable"]
src/mini_lsm_store/store.py:10:class SSTable:
src/mini_lsm_store/store.py:42:class MiniLSMStore:
src/mini_lsm_store/store.py:48:        self.sstables: list[SSTable] = []
src/mini_lsm_store/store.py:57:            table = SSTable(path)
src/mini_lsm_store/store.py:91:        table = SSTable(SSTable.file_name(self.data_dir, self._next_sequence))
src/mini_lsm_store/store.py:114:        store = MiniLSMStore(temp_dir, 32)
```

검증 신호:

- `SSTable` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `active memtable이 threshold를 넘을 때 immutable swap과 flush가 어떻게 이어지는지 익힙니다.`

핵심 코드:

```python
class SSTable:
    path: Path
    index: dict[str, str | None] | None = None

    @classmethod
    def file_name(cls, data_dir: Path, sequence: int) -> Path:
        return data_dir / f"{sequence:06d}.sst"

    def write(self, records: list[tuple[str, str | None]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            for key, value in records:
                handle.write(json.dumps({"key": key, "value": value}) + "\n")
        self.index = {key: value for key, value in records}
```

왜 이 코드가 중요했는가:

`SSTable`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Read Path`에서 정리한 요점처럼, 먼저 active MemTable을 본다.

다음:

- `MiniLSMStore`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `MiniLSMStore`가 `SSTable`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/01-mini-lsm-store/src/mini_lsm_store/store.py`의 `MiniLSMStore`
- 처음 가설:
  `MiniLSMStore`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `SSTable`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

CLI:

```bash
$ rg -n "^(class|def) " src
src/mini_lsm_store/store.py:10:class SSTable:
src/mini_lsm_store/store.py:42:class MiniLSMStore:
src/mini_lsm_store/store.py:112:def demo() -> None:
```

검증 신호:

- `MiniLSMStore`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `test_persistence_after_reopen` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```python
class MiniLSMStore:
    def __init__(self, data_dir: str | Path, memtable_size_threshold: int = 64 * 1024) -> None:
        self.data_dir = Path(data_dir)
        self.memtable_size_threshold = memtable_size_threshold or 64 * 1024
        self.memtable: dict[str, str | None] = {}
        self.immutable_memtable: dict[str, str | None] | None = None
        self.sstables: list[SSTable] = []
        self._next_sequence = 1
        self._byte_size = 0
```

왜 이 코드가 중요했는가:

`MiniLSMStore`가 없으면 `SSTable`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Read Path`에서 정리한 요점처럼, 먼저 active MemTable을 본다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
