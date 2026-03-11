# 02 WAL Recovery

append-before-apply WAL과 replay 기반 recovery를 구현해 durable write path를 만듭니다.

## 문제

- PUT/DELETE는 memtable 반영 전에 WAL에 먼저 기록돼야 합니다.
- 레코드는 checksum, type, key/value 길이, payload를 포함해야 합니다.
- replay는 첫 손상 레코드에서 멈추고 그 뒤는 버려야 합니다.
- flush 후에는 기존 WAL을 제거하거나 회전하고 새 active WAL을 열어야 합니다.

## 내 해법

- acknowledged write를 잃지 않기 위한 append-before-apply 순서를 익힙니다.
- CRC32와 레코드 헤더를 이용해 손상 지점을 감지하는 방법을 이해합니다.
- flush 이후 WAL rotation이 왜 필요한지 확인합니다.

## 검증

```bash
cd python/database-internals/projects/02-wal-recovery
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U pytest
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m wal_recovery
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

- 현재 범위 밖: group commit, fsync batching, 압축 로그 세그먼트는 포함하지 않습니다.
- 현재 범위 밖: 복수 writer와 distributed recovery는 다루지 않습니다.
- 확장 아이디어: fsync 정책, segmented WAL, recovery report를 추가하면 durability 설계 경험을 더 잘 보여 줄 수 있습니다.
- 확장 아이디어: 성능과 안정성 trade-off를 문서화하면 운영 관점 포트폴리오로 확장하기 좋습니다.
