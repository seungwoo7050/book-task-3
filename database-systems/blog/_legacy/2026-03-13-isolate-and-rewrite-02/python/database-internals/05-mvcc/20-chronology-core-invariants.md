# 20 05 MVCC의 핵심 invariant를 코드에서 고정하기

이 글은 프로젝트 전체의 가운데에 해당한다. 여기서는 README 문장을 다시 요약하지 않고, 실제 구현에서 상태 전이가 어디서 강제되는지만 따라간다.

## Phase 2
### Session 1

- 당시 목표:
  `Version`가 어떤 입력을 받아 어떤 상태를 고정하는지 분해한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/05-mvcc/src/mvcc_lab/core.py`의 `Version`
- 처음 가설:
  `Version` 하나를 이해하면 나머지 흐름도 거의 자동으로 따라올 거라고 생각했다.
- 실제 진행:
  `rg -n "Version|VersionStore" src`로 핵심 함수 위치를 다시 잡고, `Version`가 문제 정의의 첫 번째 bullet과 정확히 맞물리는지 확인했다.

CLI:

```bash
$ rg -n "Version|VersionStore" src
src/mvcc_lab/core.py:7:class Version:
src/mvcc_lab/core.py:13:class VersionStore:
src/mvcc_lab/core.py:15:        self.store: dict[str, list[Version]] = {}
src/mvcc_lab/core.py:22:        chain.insert(index, Version(value, tx_id, deleted))
src/mvcc_lab/core.py:24:    def get_visible(self, key: str, snapshot: int, committed: dict[int, bool]) -> Version | None:
src/mvcc_lab/core.py:27:                return Version(version.value, version.tx_id, version.deleted)
src/mvcc_lab/core.py:59:        self.version_store = VersionStore()
src/mvcc_lab/__init__.py:1:from .core import TransactionManager, VersionStore
src/mvcc_lab/__init__.py:3:__all__ = ["TransactionManager", "VersionStore"]
```

검증 신호:

- `Version` 안에서 상태가 한 번에 굳는지, 아니면 보조 구조로 넘겨지는지가 프로젝트의 설명 밀도를 갈랐다.
- `snapshot timestamp가 어떤 version을 볼 수 있는지 판단하는 규칙을 익힙니다.`

핵심 코드:

```python
class Version:
    value: object
    tx_id: int
    deleted: bool


class VersionStore:
    def __init__(self) -> None:
        self.store: dict[str, list[Version]] = {}
```

왜 이 코드가 중요했는가:

`Version`는 이 프로젝트의 write path 혹은 primary decision point를 드러낸다. 테스트가 요구하는 첫 번째 조건을 만족시키는 규칙이 여기서 한 번에 보였다.

새로 배운 것:

- `Write Conflict`에서 정리한 요점처럼, 이 프로젝트는 first-committer-wins 규칙을 사용한다.

다음:

- `VersionStore`까지 읽어야 비로소 이 프로젝트가 '쓰는 방법'만이 아니라 '읽고 복원하는 방법'까지 같이 고정하는지 판단할 수 있다.

### Session 2

- 당시 목표:
  `VersionStore`가 `Version`와 어떤 짝을 이루는지 확인한다.
- 변경 단위:
  `database-systems/python/database-internals/projects/05-mvcc/src/mvcc_lab/core.py`의 `VersionStore`
- 처음 가설:
  `VersionStore`는 단순 보조 함수일 거라고 생각했다.
- 실제 진행:
  두 번째 앵커를 읽고 나니, 실제로는 `Version`가 만든 상태를 외부에서 관찰 가능하게 만드는 규칙이 여기 있었다.

CLI:

```bash
$ rg -n "^(class|def) " src
src/mvcc_lab/core.py:7:class Version:
src/mvcc_lab/core.py:13:class VersionStore:
src/mvcc_lab/core.py:50:class Transaction:
src/mvcc_lab/core.py:56:class TransactionManager:
src/mvcc_lab/core.py:125:def demo() -> None:
```

검증 신호:

- `VersionStore`는 테스트의 뒤쪽 시나리오를 설명하는 열쇠였다.
- 특히 `test_abort_and_delete` 같은 이름이 왜 필요한지, 이 함수에서야 연결이 됐다.

핵심 코드:

```python
class VersionStore:
    def __init__(self) -> None:
        self.store: dict[str, list[Version]] = {}

    def append(self, key: str, value: object, tx_id: int, deleted: bool) -> None:
        chain = self.store.setdefault(key, [])
        index = 0
        while index < len(chain) and chain[index].tx_id > tx_id:
            index += 1
        chain.insert(index, Version(value, tx_id, deleted))
```

왜 이 코드가 중요했는가:

`VersionStore`가 없으면 `Version`의 의미도 끝까지 설명되지 않는다. 이 코드를 보고 나서야, 이 프로젝트가 단일 API 구현이 아니라 ordering / visibility / recovery 규칙을 통째로 묶는 이유를 납득할 수 있었다.

새로 배운 것:

- `Write Conflict`에서 정리한 요점처럼, 이 프로젝트는 first-committer-wins 규칙을 사용한다.

다음:

- 실제 재검증 명령을 다시 돌려, 지금까지 읽은 invariant가 테스트와 demo 출력에서 같은 모양으로 보이는지 확인한다.
