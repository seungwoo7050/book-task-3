# 학습 노트 안내

이 노트 묶음은 Python `05-mvcc`를 다시 구현하는 사람을 위한 재현용 설명서입니다. 이 프로젝트는 한 파일 안에 version chain, snapshot visibility, conflict detection, GC가 모두 들어 있어 “한 번 읽고 직접 다시 만들어 보기”에 특히 좋습니다.

## 왜 05가 재현성에 좋은가
- 핵심 구현이 `../src/mvcc_lab/core.py` 한 파일에 압축돼 있습니다.
- 테스트 7개가 MVCC 규칙을 거의 항목별로 대응합니다.
- 데모 출력이 짧고 명확합니다. `{'tx': 1, 'read_your_own_write': 10}` 한 줄로 가장 중요한 성질 하나를 바로 확인할 수 있습니다.

## 권장 재현 순서
1. `../problem/README.md`와 `../docs/concepts/snapshot-visibility.md`를 먼저 읽어 용어를 맞춥니다.
2. `../src/mvcc_lab/core.py`에서 `Version`, `VersionStore`, `Transaction`, `TransactionManager` 순으로 읽습니다.
3. `../tests/test_mvcc.py`에서 각 규칙이 어떤 시나리오로 검증되는지 확인합니다.
4. `../src/mvcc_lab/__main__.py`를 실행해 read-your-own-write 데모를 직접 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 구현과 학습 포인트를 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 재현 목표, 핵심 시나리오, 성공 기준을 정리합니다.
- `01-approach-log.md`: 어떤 순서로 구현을 쌓아야 재현이 쉬운지 단계별로 설명합니다.
- `02-debug-log.md`: snapshot, conflict, abort, GC가 깨질 때 보이는 증상을 기록합니다.
- `03-retrospective.md`: 왜 이 단계가 재현성 학습에 적합한지와 단순화한 지점을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 명령, 기대 출력, 테스트 맵을 한 번에 찾을 수 있게 정리합니다.

## 바로 확인할 명령
```bash
cd python/database-internals/05-mvcc
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[dev]'
PYTHONPATH=src python -m pytest tests/test_mvcc.py -v
PYTHONPATH=src python -m mvcc_lab
```

## 기대 출력
```text
{'tx': 1, 'read_your_own_write': 10}
```

## 검증 앵커
- 테스트: `test_basic_read_write`, `test_snapshot_isolation`, `test_latest_committed_value`, `test_write_write_conflict`, `test_abort_and_delete`, `test_gc`
- 데모 경로: `../src/mvcc_lab/__main__.py`
- 개념 문서: `../docs/concepts/snapshot-visibility.md`, `../docs/concepts/write-conflict.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있고, 여기서는 다시 구현할 때 바로 필요한 정보만 남깁니다.
