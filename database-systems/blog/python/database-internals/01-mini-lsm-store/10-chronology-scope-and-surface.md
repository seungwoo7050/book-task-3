# 10 01 Mini LSM Store를 읽기 전에 범위를 다시 좁히기

이 시리즈의 첫 글이다. README를 바로 요약하기보다, 테스트 이름과 파일 배치를 먼저 훑어 이 프로젝트의 테두리를 다시 그린다.

## Phase 1 — 범위를 다시 세우는 구간

이번 글에서는 먼저 테스트와 파일 구조로 문제의 테두리를 다시 잡고, 이어서 중심 타입이 어떤 책임을 끌어안는지 확인한다.

### Session 1 — 테스트와 파일 구조로 범위를 다시 좁히기

이 구간에서 먼저 붙잡으려 한 것은 `01 Mini LSM Store`가 어떤 invariant를 먼저 고정하는 슬롯인지 파악하는 것이었다. 처음 읽을 때는 구현이 너무 작아서 단순 API 연습에 가까울 거라고 봤다.

그런데 `find src tests -type f | sort`로 구조를 펼친 뒤 `rg -n "^def test_" tests`로 테스트 이름을 나열했다. 특히 `test_persistence_after_reopen`까지 테스트 이름을 훑고 나니, 이 프로젝트의 중심이 단순 기능 추가가 아니라 `SSTable` 주변의 invariant를 고정하는 일이라는 게 보였다. 이때 가장 크게 작동한 단서는 `test_put_and_get`는 가장 기본 표면을 보여 줬고, `test_persistence_after_reopen`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.

변경 단위:
- `database-systems/python/database-internals/projects/01-mini-lsm-store/README.md`, `database-systems/python/database-internals/projects/01-mini-lsm-store/tests/test_mini_lsm_store.py`

CLI:

```bash
$ find src tests -type f | sort
src/mini_lsm_store/__init__.py
src/mini_lsm_store/__main__.py
src/mini_lsm_store/__pycache__/__init__.cpython-312.pyc
src/mini_lsm_store/__pycache__/__init__.cpython-314.pyc
src/mini_lsm_store/__pycache__/__main__.cpython-312.pyc
src/mini_lsm_store/__pycache__/__main__.cpython-314.pyc
src/mini_lsm_store/__pycache__/store.cpython-312.pyc
src/mini_lsm_store/__pycache__/store.cpython-314.pyc
src/mini_lsm_store/store.py
tests/__pycache__/test_mini_lsm_store.cpython-312-pytest-8.3.5.pyc
tests/__pycache__/test_mini_lsm_store.cpython-312-pytest-9.0.2.pyc
tests/__pycache__/test_mini_lsm_store.cpython-314-pytest-9.0.2.pyc
tests/test_mini_lsm_store.py
```

```bash
$ rg -n "^def test_" tests
tests/test_mini_lsm_store.py:4:def test_put_and_get(tmp_path):
tests/test_mini_lsm_store.py:12:def test_missing_key(tmp_path):
tests/test_mini_lsm_store.py:19:def test_update(tmp_path):
tests/test_mini_lsm_store.py:28:def test_delete(tmp_path):
tests/test_mini_lsm_store.py:37:def test_flush_creates_sstable(tmp_path):
tests/test_mini_lsm_store.py:44:def test_read_after_force_flush(tmp_path):
tests/test_mini_lsm_store.py:54:def test_memtable_wins_over_sstable(tmp_path):
tests/test_mini_lsm_store.py:64:def test_tombstone_across_levels(tmp_path):
tests/test_mini_lsm_store.py:74:def test_persistence_after_reopen(tmp_path):
```

검증 신호:
- `test_put_and_get`는 가장 기본 표면을 보여 줬고, `test_persistence_after_reopen`는 이 프로젝트가 이미 경계 조건까지 포함한다는 신호였다.
- 테스트 이름만으로도 문제의 중심이 `SSTable` 주변의 ordering / visibility 규칙이라는 점이 드러났다.

핵심 코드:

```python
def test_persistence_after_reopen(tmp_path):
    store = open_store(tmp_path, 1024)
    store.put("persist", "me")
    store.close()

    reopened = MiniLSMStore(tmp_path, 1024)
    reopened.open()
    value, found = reopened.get("persist")
    assert found is True
    assert value == "me"
```

왜 여기서 판단이 바뀌었는가:

`test_persistence_after_reopen`는 README의 추상 설명보다 더 직접적으로, 어떤 실패를 막아야 하는지 보여 준다. 나는 여기서 구현 순서를 거꾸로 세우기보다 테스트가 요구하는 경계를 먼저 고정해야 한다고 판단했다.

이번 구간에서 새로 이해한 것:
- `Flush Lifecycle`에서 정리한 요점처럼, active MemTable은 write를 받는 유일한 구조다.

다음으로 넘긴 질문:
- `SSTable`와 `MiniLSMStore`를 코드에서 직접 확인해, 테스트 이름이 가리키는 invariant가 실제로 어디에 박혀 있는지 본다.

### Session 2 — 중심 타입에서 책임이 모이는 지점 보기

여기서 가장 먼저 확인한 것은 소스 파일의 중심 타입/클래스가 어떤 책임을 한곳에 묶고 있는지 확인한다. 처음에는 구현이 작으면 책임도 단순하게 한 줄로 설명될 거라고 생각했다.

하지만 실제로는 가장 큰 구현 파일인 `database-systems/python/database-internals/projects/01-mini-lsm-store/src/mini_lsm_store/store.py`를 먼저 읽고, 테스트가 요구한 상태 전이가 정말 이 파일 안에서 닫히는지 확인했다. 결정적으로 방향을 잡아 준 신호는 `SSTable` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.

변경 단위:
- `database-systems/python/database-internals/projects/01-mini-lsm-store/src/mini_lsm_store/store.py`

CLI:

```bash
$ rg -n "^(class|def) " src
src/mini_lsm_store/store.py:10:class SSTable:
src/mini_lsm_store/store.py:42:class MiniLSMStore:
src/mini_lsm_store/store.py:112:def demo() -> None:
```

검증 신호:
- `SSTable` 같은 이름이 초기에 바로 보이면 write path의 중심이 선명해진다.
- 반대로 `MiniLSMStore`가 함께 보이면 read path나 visibility 규칙을 따로 떼어 설명할 수 없다는 뜻이다.

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

왜 여기서 판단이 바뀌었는가:

`SSTable`는 이 프로젝트가 가장 먼저 고정해야 하는 상태 전이를 보여 준다. 이 조각을 보고 나서야 테스트 이름과 구현 책임이 같은 문제를 가리키고 있다는 확신이 생겼다.

이번 구간에서 새로 이해한 것:
- `Read Path`에서 정리한 요점처럼, 먼저 active MemTable을 본다.

다음으로 넘긴 질문:
- 같은 상태를 반대 방향에서 고정하는 `MiniLSMStore`를 읽어, write/read 혹은 append/replay가 서로 어떻게 잠기는지 확인한다.
