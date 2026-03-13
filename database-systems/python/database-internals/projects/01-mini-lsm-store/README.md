# 01 Mini LSM Store

active memtable, immutable flush, newest-first read path를 연결해 최소 LSM store를 완성합니다.

## 문제

- active memtable이 threshold를 넘으면 immutable swap 후 SSTable로 flush해야 합니다.
- read path는 active memtable, immutable memtable, newest SSTable부터 순서대로 조회해야 합니다.
- tombstone은 cross-level read에서도 삭제 의미를 유지해야 합니다.
- close 이후 re-open 시 기존 SSTable index를 다시 적재해야 합니다.

## 내 해법

- active memtable이 threshold를 넘을 때 immutable swap과 flush가 어떻게 이어지는지 익힙니다.
- active/immutable/SSTable을 newest-first로 읽는 read path를 구성합니다.
- close 이후 re-open 시 persisted metadata를 다시 적재하는 흐름을 확인합니다.

## 검증

```bash
cd python/database-internals/projects/01-mini-lsm-store
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U pytest
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m mini_lsm_store
```

## 코드 지도

- `problem/README.md`: 문제 정의, 제약, 제공 자료, provenance를 확인하는 시작점입니다.
- `docs/README.md`: 개념 메모와 참고자료 인덱스를 먼저 훑는 문서입니다.
- `src/`: 핵심 구현 패키지와 `__main__` entry point가 들어 있습니다.
- `tests/`: pytest 기반 회귀 테스트를 모아 둔 위치입니다.
- `../../../../blog/python/database-internals/01-mini-lsm-store/00-series-map.md`: `src/tests`와 실제 재검증 CLI만으로 다시 구성한 source-first blog 시리즈 입구입니다.
- `notion/README.md`: 현재 공개용 학습 노트와 설계 로그의 입구입니다.
- `notion-archive/README.md`: 이전 세대 문서를 보존하는 아카이브입니다.

## 읽는 순서

- `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
- `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
- `src/`와 `tests/`를 함께 읽고, 마지막에 패키지 entry point를 실행해 전체 흐름을 확인합니다.
- `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 한계와 확장

- 현재 범위 밖: background compaction과 concurrent flush는 다루지 않습니다.
- 현재 범위 밖: range query와 compression 같은 production 기능은 후속 확장 항목으로 남깁니다.
- 확장 아이디어: manifest 파일과 background compaction을 추가하면 더 현실적인 mini storage engine으로 확장할 수 있습니다.
- 확장 아이디어: flush/lookup 지표를 수집해 성능 관찰 포인트를 넣으면 포트폴리오 설득력이 높아집니다.
