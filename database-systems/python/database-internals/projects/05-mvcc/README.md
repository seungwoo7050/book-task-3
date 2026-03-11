# 05 MVCC

snapshot isolation을 위한 version chain과 transaction manager를 구현합니다.

## 문제

- snapshot isolation 하에서 읽기 스냅샷과 write-write conflict를 관리해야 합니다.
- read-your-own-write를 보장해야 합니다.
- first-committer-wins conflict detection이 필요합니다.
- aborted version cleanup과 stale version GC가 동작해야 합니다.

## 내 해법

- snapshot timestamp가 어떤 version을 볼 수 있는지 판단하는 규칙을 익힙니다.
- first-committer-wins 충돌 판정을 이해합니다.
- stale version GC가 왜 필요한지 확인합니다.

## 검증

```bash
cd python/database-internals/projects/05-mvcc
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U pytest
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m mvcc_lab
```

## 코드 지도

- `problem/README.md`: 문제 정의, 제약, 제공 자료, provenance를 확인하는 시작점입니다.
- `docs/README.md`: 개념 메모와 참고자료 인덱스를 먼저 훑는 문서입니다.
- `src/`: 핵심 구현 패키지와 `__main__` entry point가 들어 있습니다.
- `tests/`: pytest 기반 회귀 테스트를 모아 둔 위치입니다.
- `notion/README.md`: 현재 공개용 학습 노트와 설계 로그의 입구입니다.
- `notion-archive/README.md`: 이전 세대 문서를 보존하는 아카이브입니다.

## 읽는 순서

- `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
- `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
- `src/`와 `tests/`를 함께 읽고, 마지막에 패키지 entry point를 실행해 전체 흐름을 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: predicate locking, phantom read 제어, distributed transaction은 포함하지 않습니다.
- 현재 범위 밖: full SQL transaction manager나 lock table은 후속 확장 범위입니다.
- 확장 아이디어: lock manager, transaction state visualizer, long-running read 시나리오를 추가하면 깊이가 생깁니다.
- 확장 아이디어: 격리 수준 비교 실험을 문서화하면 학습 레포에서 포트폴리오 레포로 옮기기 좋습니다.
