# 05 MVCC — 개발 타임라인

## Phase 0: 환경 준비

```bash
cd python/database-internals/projects/05-mvcc
python3 --version
# Python 3.14.x

python3 -m pip install -U pytest
```

### 디렉토리 구조 생성

```bash
mkdir -p src/mvcc_lab tests docs/concepts docs/references
touch src/mvcc_lab/__init__.py
touch src/mvcc_lab/__main__.py
touch src/mvcc_lab/core.py
touch tests/test_mvcc.py
```

**결정**: 패키지명 `mvcc_lab`. `mvcc`는 너무 짧고 충돌 가능성이 있어 `_lab` 접미사 추가.

---

## Phase 1: Version과 VersionStore

### 1.1 Version dataclass

```python
@dataclass(slots=True)
class Version:
    value: object
    tx_id: int
    deleted: bool
```

세 가지 정보: 값, 생성한 트랜잭션 ID, 삭제 여부.

### 1.2 VersionStore

```python
class VersionStore:
    def __init__(self) -> None:
        self.store: dict[str, list[Version]] = {}
```

`dict[str, list[Version]]` — 키별 version chain. 리스트는 tx_id 내림차순으로 유지.

### 1.3 append — 삽입 정렬

```python
def append(self, key: str, value: object, tx_id: int, deleted: bool) -> None:
    chain = self.store.setdefault(key, [])
    index = 0
    while index < len(chain) and chain[index].tx_id > tx_id:
        index += 1
    chain.insert(index, Version(value, tx_id, deleted))
```

**결정**: tx_id 내림차순 유지를 위해 삽입 정렬. 대부분의 경우 최신 tx_id가 들어오므로 index=0에서 바로 삽입되어 O(1).

### 1.4 get_visible — 가시성 검사

```python
def get_visible(self, key: str, snapshot: int, committed: dict[int, bool]) -> Version | None:
    for version in self.store.get(key, []):
        if version.tx_id <= snapshot and committed.get(version.tx_id, False):
            return Version(version.value, version.tx_id, version.deleted)
    return None
```

내림차순이므로 첫 번째 만족하는 버전이 가장 최신.

### 1.5 remove_by_tx_id — abort 지원

```python
def remove_by_tx_id(self, key: str, tx_id: int) -> None:
    filtered = [v for v in self.store.get(key, []) if v.tx_id != tx_id]
```

특정 tx_id의 모든 버전을 제거. abort 시 호출.

### 1.6 gc — 이전 버전 정리

```python
def gc(self, min_snapshot: int) -> None:
```

`min_snapshot` 이전 버전 중 가장 최신 하나만 보존. 나머지 삭제.

---

## Phase 2: Transaction과 TransactionManager

### 2.1 Transaction dataclass

```python
@dataclass(slots=True)
class Transaction:
    snapshot: int
    status: str
    write_set: set[str] = field(default_factory=set)
```

**결정**: `write_set`을 `set[str]`로. Go의 `map[string]struct{}`와 동일한 역할. 커밋 시 conflict 검사 대상.

### 2.2 begin

```python
def begin(self) -> int:
    tx_id = self.next_tx_id
    self.next_tx_id += 1
    snapshot = max(self.committed, default=0)
    self.transactions[tx_id] = Transaction(snapshot=snapshot, status="active")
    return tx_id
```

`max(self.committed, default=0)` — committed dict의 키 중 최대값이 스냅샷. 커밋된 트랜잭션이 없으면 0.

### 2.3 read — read-your-own-write 우선

```python
def read(self, tx_id: int, key: str):
    tx = self._active_tx(tx_id)
    if key in tx.write_set:
        # 자신이 쓴 버전을 직접 찾기
        for version in self.version_store.store.get(key, []):
            if version.tx_id == tx_id:
                return None if version.deleted else version.value
    # 스냅샷 기반 가시성
    version = self.version_store.get_visible(key, tx.snapshot, self.committed)
```

### 2.4 write / delete

```python
def write(self, tx_id: int, key: str, value) -> None:
    self.version_store.append(key, value, tx_id, False)
    tx.write_set.add(key)

def delete(self, tx_id: int, key: str) -> None:
    self.version_store.append(key, None, tx_id, True)
    tx.write_set.add(key)
```

delete는 `deleted=True` 버전 추가. 물리적 삭제 아님.

### 2.5 commit — first-committer-wins

```python
def commit(self, tx_id: int) -> None:
    for key in tx.write_set:
        for version in self.version_store.store.get(key, []):
            if version.tx_id > tx.snapshot and version.tx_id != tx_id and self.committed.get(version.tx_id, False):
                self._abort_internal(tx_id, tx)
                raise ValueError(f'write-write conflict on key "{key}"')
    tx.status = "committed"
    self.committed[tx_id] = True
```

세 조건: (1) 스냅샷 이후 (2) 자기 아님 (3) 이미 커밋됨 → 충돌.

### 2.6 abort

```python
def _abort_internal(self, tx_id: int, tx: Transaction) -> None:
    for key in tx.write_set:
        self.version_store.remove_by_tx_id(key, tx_id)
    tx.status = "aborted"
```

write_set의 모든 키에서 해당 tx_id 버전 제거.

---

## Phase 3: 테스트 작성 및 검증

### 3.1 기본 read/write

```bash
PYTHONPATH=src python3 -m pytest tests/test_mvcc.py::test_basic_read_write -v
```

write → read-your-own-write 확인, 없는 키는 None.

### 3.2 snapshot isolation

```bash
PYTHONPATH=src python3 -m pytest tests/test_mvcc.py::test_snapshot_isolation -v
```

t3가 커밋해도 t2는 이전 값(100)을 봄.

### 3.3 latest committed value

```bash
PYTHONPATH=src python3 -m pytest tests/test_mvcc.py::test_latest_committed_value -v
```

순차 커밋 후 새 트랜잭션은 최신 값("v2")을 봄.

### 3.4 write-write conflict

```bash
PYTHONPATH=src python3 -m pytest tests/test_mvcc.py::test_write_write_conflict -v
```

같은 키 수정 → 먼저 커밋한 쪽 승리, 나중 쪽 ValueError.

### 3.5 different keys no conflict

```bash
PYTHONPATH=src python3 -m pytest tests/test_mvcc.py::test_different_keys_no_conflict -v
```

다른 키면 충돌 없이 양쪽 커밋 성공.

### 3.6 abort and delete

```bash
PYTHONPATH=src python3 -m pytest tests/test_mvcc.py::test_abort_and_delete -v
```

abort된 값은 보이지 않음. delete 후 None 반환.

### 3.7 gc

```bash
PYTHONPATH=src python3 -m pytest tests/test_mvcc.py::test_gc -v
```

GC 후 version chain 길이가 줄어드는지 확인.

### 3.8 전체 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/ -v
```

7개 테스트 모두 통과 확인.

---

## Phase 4: Demo

### 4.1 __main__.py

```python
from .core import demo

if __name__ == "__main__":
    demo()
```

### 4.2 demo 실행

```bash
PYTHONPATH=src python3 -m mvcc_lab
# {"tx": 1, "read_your_own_write": 10}
```

---

## Phase 5: 개념 문서 작성

### docs/concepts/snapshot-visibility.md
- 스냅샷 시점 결정 방법
- 가시성 규칙 두 조건

### docs/concepts/write-conflict.md
- first-committer-wins 정책
- 충돌 검사 세 조건

---

## 소스코드에서 드러나지 않는 결정들

1. **`max(self.committed, default=0)`**: committed dict의 키(tx_id) 중 최대값으로 스냅샷 결정. 단순하지만 정확한 이유 — committed에 tx_id가 추가되는 순서가 단조 증가하므로 max가 항상 최신 커밋.

2. **version chain 정렬 방향**: tx_id 내림차순. 오름차순으로 해도 동작하지만, 가시성 검사에서 최신부터 찾아야 하므로 내림차순이 자연스러움.

3. **abort 시 version 제거**: 커밋 표시만 안 하면 다른 트랜잭션에게 안 보이지만, GC 부담을 줄이기 위해 즉시 제거.

4. **GC에서 old 버전 하나 보존**: `old[0]` (가장 최신 old)을 유지. 이유 — min_snapshot 시점에 시작된 활성 트랜잭션이 이 버전을 읽을 가능성.

5. **외부 의존성 없음**: hashlib, struct 등 불필요. 순수 Python dict와 list만으로 전체 MVCC 구현. 이전 프로젝트들과 달리 바이너리 직렬화가 필요 없는 in-memory 전용.

6. **`value: object` 타입**: 문자열, 정수, 어떤 타입이든 저장 가능. Go의 `any`와 동일한 설계. 테스트에서 정수와 문자열을 혼용하여 타입 무관성 증명.
