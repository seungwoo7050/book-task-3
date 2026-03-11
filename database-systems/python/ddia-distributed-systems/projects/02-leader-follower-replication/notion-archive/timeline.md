# 02 Leader-Follower Replication — 개발 타임라인

## Phase 0: 환경 준비

```bash
cd python/ddia-distributed-systems/projects/02-leader-follower-replication
python3 --version
# Python 3.14.x

python3 -m pip install -U pytest
```

### 디렉토리 구조 생성

```bash
mkdir -p src/leader_follower tests docs/concepts docs/references
touch src/leader_follower/__init__.py
touch src/leader_follower/__main__.py
touch src/leader_follower/core.py
touch tests/test_replication.py
```

---

## Phase 1: LogEntry와 ReplicationLog

### 1.1 LogEntry dataclass

```python
@dataclass(slots=True)
class LogEntry:
    offset: int
    operation: str    # "put" | "delete"
    key: str
    value: str | None  # delete일 때 None
```

**결정**: Go의 `*string` 대신 `str | None` union type. Python의 표준적인 nullable 패턴.

### 1.2 ReplicationLog

```python
class ReplicationLog:
    def __init__(self) -> None:
        self.entries: list[LogEntry] = []

    def append(self, operation: str, key: str, value: str | None) -> int:
        offset = len(self.entries)
        self.entries.append(LogEntry(offset, operation, key, value))
        return offset
```

offset = list index. 별도 카운터 불필요.

### 1.3 로그 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_replication.py::test_replication_log_assigns_sequential_offsets -v
```

순차 offset 할당 확인 (0, 1, ...).

---

## Phase 2: Leader

### 2.1 store + log 동시 관리

```python
class Leader:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.log = ReplicationLog()

    def put(self, key: str, value: str) -> int:
        self.store[key] = value
        return self.log.append("put", key, value)
```

**결정**: store 적용과 log 기록을 하나의 메서드에서 수행. 순서: store 먼저 → log 기록. 역순이면 log에는 있는데 store에는 없는 상태가 발생할 수 있음.

### 2.2 delete

```python
def delete(self, key: str) -> int:
    self.store.pop(key, None)
    return self.log.append("delete", key, None)
```

없는 키 삭제도 에러 없이 처리. log에 기록하여 follower가 삭제를 적용할 수 있게 함.

### 2.3 log_from과 latest_offset

leader가 follower에게 "이 offset 이후의 엔트리"를 제공하는 인터페이스.

---

## Phase 3: Follower

### 3.1 watermark 패턴

```python
class Follower:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.last_applied_offset = -1
```

`-1`은 "아직 아무것도 적용하지 않음".

### 3.2 idempotent apply

```python
def apply(self, entries: list[LogEntry]) -> int:
    for entry in entries:
        if entry.offset <= self.last_applied_offset:
            continue
        # ... operation 적용 ...
        self.last_applied_offset = entry.offset
```

핵심 한 줄: `if entry.offset <= self.last_applied_offset: continue`

### 3.3 멱등성 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_replication.py::test_follower_apply_is_idempotent -v
```

같은 entries를 두 번 적용: 첫 번째 2개, 두 번째 0개.

---

## Phase 4: replicate_once 통합

### 4.1 함수 하나로 동기화

```python
def replicate_once(leader: Leader, follower: Follower) -> int:
    entries = leader.log_from(follower.watermark() + 1)
    return follower.apply(entries)
```

3줄로 전체 복제 사이클 완성:
1. follower의 watermark + 1부터 로그 요청
2. follower에게 적용
3. 적용된 엔트리 수 반환

### 4.2 통합 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/test_replication.py::test_replicate_once_incremental_and_deletes -v
```

시나리오:
1. leader.put("a", "1") → replicate → follower에 "a"="1"
2. leader.put("b", "2") + leader.delete("a") → replicate → follower에 "a" 삭제, "b"="2"

---

## Phase 5: Demo와 마무리

### 5.1 demo 실행

```bash
PYTHONPATH=src python3 -m leader_follower
# {"applied": 1, "value": "1"}
```

### 5.2 전체 테스트

```bash
PYTHONPATH=src python3 -m pytest tests/ -v
```

3개 테스트 모두 통과 확인.

---

## 소스코드에서 드러나지 않는 결정들

1. **in-memory 전용**: 네트워크 없이 로컬에서 동작. 실제 분산 시스템에서는 01-rpc-framing 위에 올라가야 하지만, 복제 로직 자체의 정확성을 먼저 검증.

2. **offset = list index**: 별도의 카운터나 atomic 변수 없이 `len(self.entries)`를 offset으로 사용. 단일 스레드 환경에서 가장 단순한 선택.

3. **get() 반환 패턴**: `(str, bool)` — 값과 존재 여부. Go 스타일의 `(value, ok)` 패턴을 Python으로 그대로 옮김.

4. **idempotent apply의 중요성**: 네트워크 재전송, 복구 시 같은 엔트리를 다시 받을 수 있음. offset 비교 한 줄이 이 문제를 해결.

5. **delete의 log 기록**: store에서 삭제한 것만으로는 follower가 모름. log에 "delete" operation을 기록해야 follower도 삭제할 수 있음.

6. **replicate_once가 별도 함수인 이유**: Leader나 Follower의 메서드가 아닌 독립 함수. 둘 사이의 결합도를 낮추고, 호출 시점을 caller가 제어.
