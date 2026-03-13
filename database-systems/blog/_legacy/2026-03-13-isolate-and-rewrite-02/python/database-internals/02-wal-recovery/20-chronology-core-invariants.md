# 20 02 WAL Recovery의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `WALRecord`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/02-wal-recovery/src/wal_recovery/store.py`의 `WALRecord`
- 처음 가설:
  `WALRecord` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "WALRecord|WriteAheadLog" src`로 핵심 함수 위치를 다시 잡고, `WALRecord`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "WALRecord|WriteAheadLog" src
src/wal_recovery/__init__.py:1:from .store import DurableStore, WriteAheadLog
src/wal_recovery/__init__.py:3:__all__ = ["DurableStore", "WriteAheadLog"]
src/wal_recovery/store.py:16:class WALRecord:
src/wal_recovery/store.py:22:class WriteAheadLog:
src/wal_recovery/store.py:38:    def recover(self) -> list[WALRecord]:
src/wal_recovery/store.py:42:        records: list[WALRecord] = []
src/wal_recovery/store.py:62:                records.append(WALRecord("delete", key))
src/wal_recovery/store.py:65:                records.append(WALRecord("put", key, value))
src/wal_recovery/store.py:127:        self._wal = WriteAheadLog(self.wal_path, fsync_enabled)
src/wal_recovery/store.py:142:        for record in WriteAheadLog(self.wal_path, False).recover():
src/wal_recovery/store.py:177:        self._wal = WriteAheadLog(self.wal_path, self._wal.fsync_enabled)
```

검증 신호:

- `WALRecord` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `acknowledged write를 잃지 않기 위한 append-before-apply 순서를 익힙니다.`

핵심 코드:

```python
class WALRecord:
    record_type: str
    key: str
    value: str | None = None


class WriteAheadLog:
    def __init__(self, path: str | Path, fsync_enabled: bool = False) -> None:
        self.path = Path(path)
        self.fsync_enabled = fsync_enabled
        self._handle = None
```

왜 이 코드가 중요했는가:

`WALRecord`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `WAL Record Format`에서 정리한 요점처럼, record는 `[crc32][type][keyLen][valLen][key][value]` 순서다.

다음:

- `WriteAheadLog`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `WriteAheadLog`가 `WALRecord`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/02-wal-recovery/src/wal_recovery/store.py`의 `WriteAheadLog`
- 처음 가설:
  `WriteAheadLog`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `WALRecord`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

CLI:

```bash
$ rg -n "^(class|def) " src
src/wal_recovery/store.py:16:class WALRecord:
src/wal_recovery/store.py:22:class WriteAheadLog:
src/wal_recovery/store.py:87:class SSTable:
src/wal_recovery/store.py:118:class DurableStore:
src/wal_recovery/store.py:195:def demo() -> None:
```

검증 신호:

- `WriteAheadLog`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `test_force_flush_rotates_wal` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```python
class WriteAheadLog:
    def __init__(self, path: str | Path, fsync_enabled: bool = False) -> None:
        self.path = Path(path)
        self.fsync_enabled = fsync_enabled
        self._handle = None

    def open(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.path.open("ab")
```

왜 이 코드가 중요했는가:

`WriteAheadLog`가 없으면 `WALRecord`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `WAL Record Format`에서 정리한 요점처럼, record는 `[crc32][type][keyLen][valLen][key][value]` 순서다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
