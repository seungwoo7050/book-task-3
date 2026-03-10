# "데이터를 두 곳에 두는 가장 단순한 방법" — Python으로 Leader-Follower 복제

## 왜 복제가 필요한가

서버가 하나면 그 서버가 죽으면 데이터가 사라진다. 두 대 이상에 같은 데이터를 유지하면 하나가 죽어도 나머지가 서비스할 수 있다. 문제는 **어떻게 두 서버의 데이터를 동기화할 것인가**다.

가장 단순한 답: 하나를 leader로 정하고 모든 쓰기를 leader에서 받는다. leader는 변경 사항을 로그에 기록하고, follower는 이 로그를 따라간다.

## ReplicationLog: 변경의 역사

```python
@dataclass(slots=True)
class LogEntry:
    offset: int
    operation: str
    key: str
    value: str | None

class ReplicationLog:
    def __init__(self) -> None:
        self.entries: list[LogEntry] = []

    def append(self, operation: str, key: str, value: str | None) -> int:
        offset = len(self.entries)
        self.entries.append(LogEntry(offset, operation, key, value))
        return offset
```

모든 변경은 순차적 offset을 받는다. `len(self.entries)`가 곧 다음 offset이 된다. 단순하지만 결정적인 설계: **offset이 monotonic하게 증가**하므로 follower는 "어디까지 받았는지"를 하나의 숫자로 표현할 수 있다.

`from_offset()` 메서드로 특정 offset 이후의 엔트리만 가져올 수 있다:

```python
def from_offset(self, offset: int) -> list[LogEntry]:
    return list(self.entries[max(offset, 0):])
```

Go 버전과 동일한 구조다. `*string`으로 optional value를 표현한 Go와 달리, Python에서는 `str | None` union type을 사용한다.

## Leader: 쓰기와 로그 동시 관리

```python
class Leader:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.log = ReplicationLog()

    def put(self, key: str, value: str) -> int:
        self.store[key] = value
        return self.log.append("put", key, value)
```

Leader의 `put()`은 두 가지를 한다:
1. **로컬 store에 적용**: 즉시 읽기 가능
2. **로그에 기록**: follower가 나중에 따라올 수 있도록

`delete()`도 마찬가지다:

```python
def delete(self, key: str) -> int:
    self.store.pop(key, None)
    return self.log.append("delete", key, None)
```

`store.pop(key, None)`으로 없는 키 삭제 시 에러 없이 처리. 로그에는 `value=None`으로 기록.

## Follower: Watermark 기반 따라잡기

```python
class Follower:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.last_applied_offset = -1
```

`last_applied_offset = -1`로 시작. "아직 아무것도 적용하지 않았다"는 의미.

### apply: 멱등적 적용

```python
def apply(self, entries: list[LogEntry]) -> int:
    applied = 0
    for entry in entries:
        if entry.offset <= self.last_applied_offset:
            continue
        if entry.operation == "put" and entry.value is not None:
            self.store[entry.key] = entry.value
        if entry.operation == "delete":
            self.store.pop(entry.key, None)
        self.last_applied_offset = entry.offset
        applied += 1
    return applied
```

핵심은 `if entry.offset <= self.last_applied_offset: continue`. 이미 적용한 엔트리는 건너뛴다. 이 한 줄이 **멱등성(idempotency)**을 보장한다. 같은 엔트리를 두 번 받아도 결과가 달라지지 않는다.

테스트가 이를 검증한다:

```python
def test_follower_apply_is_idempotent():
    assert follower.apply(entries) == 2   # 처음: 2개 적용
    assert follower.apply(entries) == 0   # 두 번째: 0개 적용 (이미 적용됨)
```

### watermark

```python
def watermark(self) -> int:
    return self.last_applied_offset
```

follower가 "어디까지 받았는지"를 알려주는 단일 숫자. leader에게 "이 offset 이후부터 달라"고 요청할 때 사용한다.

## replicate_once: 한 번의 동기화

```python
def replicate_once(leader: Leader, follower: Follower) -> int:
    entries = leader.log_from(follower.watermark() + 1)
    return follower.apply(entries)
```

이 함수 하나가 복제의 전부다:
1. follower의 watermark + 1부터 leader의 로그를 가져온다
2. follower에게 적용한다

호출할 때마다 follower가 leader를 한 단계 따라잡는다. 테스트를 보면:

```python
leader.put("a", "1")
assert replicate_once(leader, follower) == 1    # 1개 적용

leader.put("b", "2")
leader.delete("a")
assert replicate_once(leader, follower) == 2    # 2개 적용
assert follower.get("a") == ("", False)          # 삭제됨
assert follower.get("b") == ("2", True)          # 복제됨
```

## Go 버전과의 차이

| 항목 | Go DDIA-02 | Python DDIA-02 |
|------|-----------|----------------|
| Optional value | `*string` (pointer) | `str \| None` |
| Store | `map[string]string` | `dict[str, str]` |
| 반환 패턴 | `(string, bool)` | `(str, bool)` |
| 외부 의존성 | 없음 | 없음 |
| 코드량 | ~120줄 | ~90줄 |
| 테스트 수 | 3개 | 3개 |

구조가 거의 동일하다. 언어 문법만 다르고 알고리즘은 완전히 같다.

## 마무리

Leader-follower 복제는 분산 시스템에서 가장 기초적인 복제 방식이다. append-only 로그가 변경의 순서를 보장하고, watermark가 "어디까지 받았는지"를 추적하며, 멱등적 적용이 네트워크 재전송에 대한 안전성을 제공한다.

소스코드에서 드러나지 않는 핵심: **이 세 가지(순서 있는 로그, watermark, 멱등성)는 독립적으로 설계되었지만 함께 동작할 때 비로소 안전한 복제가 된다.** 하나라도 빠지면 데이터 불일치가 발생한다. replicate_once 함수 3줄이 이 세 가지를 모두 연결하는 접착제다.
