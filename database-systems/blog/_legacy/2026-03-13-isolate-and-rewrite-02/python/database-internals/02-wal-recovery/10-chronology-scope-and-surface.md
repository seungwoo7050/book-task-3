# 10 02 WAL Recovery의 범위를 다시 잡기

이 글은 프로젝트 전체에서 가장 앞부분에 해당한다. README의 한 줄 설명을 곧바로 믿지 않고, 파일 구조와 테스트 이름만으로 먼저 범위를 다시 세운다.

## Phase 1
### Session 1

- 당시 목표:
  `02 WAL Recovery`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/02-wal-recovery/README.md`, `database-systems/python/database-internals/projects/02-wal-recovery/tests/test_wal_recovery.py`
- 처음 가설:
  구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.
- 실제 진행:
  `find src tests -type f | sort`로 구조를 펼친 뒤 `rg -n "^def test_" tests`로 테스트 이름을 나열했다. `test_force_flush_rotates_wal`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `WALRecord` 주변의 invariant를 고정하는 일이라는 게 보였다.

CLI:

```bash
$ find src tests -type f | sort
src/wal_recovery/__init__.py
src/wal_recovery/__main__.py
src/wal_recovery/__pycache__/__init__.cpython-312.pyc
src/wal_recovery/__pycache__/__init__.cpython-314.pyc
src/wal_recovery/__pycache__/__main__.cpython-312.pyc
src/wal_recovery/__pycache__/__main__.cpython-314.pyc
src/wal_recovery/__pycache__/store.cpython-312.pyc
src/wal_recovery/__pycache__/store.cpython-314.pyc
src/wal_recovery/store.py
tests/__pycache__/test_wal_recovery.cpython-312-pytest-8.3.5.pyc
tests/__pycache__/test_wal_recovery.cpython-314-pytest-9.0.2.pyc
tests/test_wal_recovery.py
```

```bash
$ rg -n "^def test_" tests
tests/test_wal_recovery.py:6:def test_recover_put_records(tmp_path):
tests/test_wal_recovery.py:20:def test_recover_delete_records(tmp_path):
tests/test_wal_recovery.py:33:def test_recover_many_records(tmp_path):
tests/test_wal_recovery.py:46:def test_stop_at_corrupted_record(tmp_path):
tests/test_wal_recovery.py:59:def test_recover_nonexistent_and_truncated(tmp_path):
tests/test_wal_recovery.py:66:def test_store_recovers_from_wal_after_reopen(tmp_path):
tests/test_wal_recovery.py:78:def test_force_flush_rotates_wal(tmp_path):
```

검증 신호:

- `test_recover_put_records`는 가장 기본 표면을 보여 줬고, `test_force_flush_rotates_wal`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `WALRecord` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```python
def test_force_flush_rotates_wal(tmp_path):
    store = DurableStore(tmp_path, 4096, False)
    store.open()
    store.put("alpha", "1")
    store.force_flush()
    wal_path = Path(tmp_path) / "active.wal"
    assert wal_path.stat().st_size == 0
    reopened = DurableStore(tmp_path, 4096, False)
    reopened.open()
    value, found = reopened.get("alpha")
    assert found is True
    assert value == "1"
```

왜 이 코드가 중요했는가:

`test_force_flush_rotates_wal`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

새로 배운 것:

- `Recovery Policy`에서 정리한 요점처럼, header가 13바이트보다 짧으면 truncated header로 보고 중단한다.

다음:

- `WALRecord`와 `WriteAheadLog`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2

- 당시 목표:
  소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/02-wal-recovery/src/wal_recovery/store.py`
- 처음 가설:
  구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.
- 실제 진행:
  가장 큰 구현 파일인 `database-systems/python/database-internals/projects/02-wal-recovery/src/wal_recovery/store.py`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다.

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

- `WALRecord` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `WriteAheadLog`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

`WALRecord`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 읽고 나서야 테스트 이름과 실제 구현 책임이 같은 축에 놓여 있다는 확신이 생겼다.

새로 배운 것:

- `WAL Record Format`에서 정리한 요점처럼, record는 `[crc32][type][keyLen][valLen][key][value]` 순서다.

다음:

- 같은 상태를 반대 방향에서 고정하는 `WriteAheadLog`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
