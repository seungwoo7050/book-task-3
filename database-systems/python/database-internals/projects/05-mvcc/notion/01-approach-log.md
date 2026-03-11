# 접근 기록

## 재현 순서 제안
이 프로젝트는 “타입 하나 만들고, 테스트 하나 맞추고, 다음 규칙으로 넘어간다”는 순서가 가장 재현하기 쉽습니다.

### 1. `Version`과 `VersionStore`만 먼저 만든다
- 관련 파일: `../src/mvcc_lab/core.py`
- 먼저 구현할 메서드:
  - `append`
  - `get_visible`
  - `remove_by_tx_id`
  - `gc`
- 이유: version chain 정렬 규칙이 맞아야 snapshot, abort, GC 전부가 단순해집니다.

### 2. `Transaction`과 `begin()`을 붙여 snapshot을 고정한다
- 관련 파일: `../src/mvcc_lab/core.py`
- 핵심 판단: `begin()`이 가장 최근 committed tx_id를 snapshot으로 잡습니다.
- 여기까지 구현한 뒤 먼저 볼 테스트:

```bash
cd python/database-internals/projects/05-mvcc
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
PYTHONPATH=src python -m pytest tests/test_mvcc.py::test_snapshot_isolation -v
```

### 3. `read()`에서 read-your-own-write를 먼저 처리한다
- 관련 파일: `../src/mvcc_lab/core.py`
- 이유: snapshot 규칙만 적용하면 자기 자신의 미커밋 write도 안 보이는 잘못된 구현이 되기 쉽습니다.
- 빠른 확인:

```bash
PYTHONPATH=src python -m pytest tests/test_mvcc.py::test_basic_read_write -v
PYTHONPATH=src python -m mvcc_lab
```

### 4. 마지막에 `commit`, `abort`, `gc`를 붙인다
- 관련 파일: `../src/mvcc_lab/core.py`, `../tests/test_mvcc.py`
- 구현 순서:
  1. `commit`에서 conflict 검사
  2. `abort`
  3. `gc`
- 닫는 명령:

```bash
PYTHONPATH=src python -m pytest tests/test_mvcc.py -v
```

## 코드가 택한 핵심 판단
### key마다 version chain 하나를 둔다
- 관련 파일: `../src/mvcc_lab/core.py`
- 판단: `dict[str, list[Version]]` 하나로도 MVCC의 핵심 visibility 규칙을 충분히 설명할 수 있습니다.

### snapshot은 begin 시점에만 정한다
- 관련 파일: `../src/mvcc_lab/core.py`
- 판단: 읽을 때마다 최신 commit을 보는 게 아니라, transaction 시작 시점의 경계를 고정해야 snapshot isolation이 설명됩니다.

### conflict는 commit에서 늦게 검증한다
- 관련 파일: `../src/mvcc_lab/core.py`
- 판단: write 시점에는 version을 추가하고, commit 시점에 같은 key의 더 새로운 committed version이 있는지만 검사하는 쪽이 학습용으로 가장 단순합니다.

## 기대 출력과 빠른 해석
데모가 정상이라면 다음이 출력됩니다.

```text
{'tx': 1, 'read_your_own_write': 10}
```

이 한 줄은 적어도 두 가지를 동시에 보여 줍니다.
- transaction이 시작되었다.
- 자기 자신이 방금 쓴 값은 snapshot 규칙보다 먼저 보인다.

## 포트폴리오 설명으로 바꿀 때 남길 장면
- `VersionStore`와 `TransactionManager` 분리는 저장 구조와 정책을 나눈 선택으로 설명할 수 있습니다.
- `test_snapshot_isolation`과 `test_write_write_conflict`는 MVCC 설명의 중심 사례로 바로 쓸 수 있습니다.
- “최신 값 하나” 모델에서 “버전 체인” 모델로 사고가 바뀌는 지점이 이 프로젝트의 핵심입니다.
