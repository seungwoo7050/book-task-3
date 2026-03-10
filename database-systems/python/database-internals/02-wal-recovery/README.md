# 02 WAL Recovery

append-before-apply WAL과 replay 기반 recovery를 구현해 durable write path를 만듭니다.

## 이 프로젝트에서 배우는 것

- acknowledged write를 잃지 않기 위한 append-before-apply 순서를 익힙니다.
- CRC32와 레코드 헤더를 이용해 손상 지점을 감지하는 방법을 이해합니다.
- flush 이후 WAL rotation이 왜 필요한지 확인합니다.

## 먼저 알고 있으면 좋은 것

- mini LSM store 수준의 쓰기/읽기 흐름을 알고 있으면 좋습니다.
- 파일 append와 binary header 같은 기초 I/O 개념이 있으면 읽기 쉽습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `src/`와 `tests/`를 함께 읽고, 마지막에 패키지 entry point를 실행해 전체 흐름을 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `src/wal_recovery/`, `tests/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd python/database-internals/02-wal-recovery
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U pytest
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m wal_recovery
```

## 구현에서 집중할 포인트

- WAL append와 memtable apply 순서가 바뀌지 않는지 확인합니다.
- 첫 손상 레코드 이후를 버리는 보수적 recovery policy를 테스트로 검증합니다.
- flush 이후 새 WAL 세그먼트로 회전하는 경계를 봅니다.

## 포트폴리오로 발전시키려면

- fsync 정책, segmented WAL, recovery report를 추가하면 durability 설계 경험을 더 잘 보여 줄 수 있습니다.
- 성능과 안정성 trade-off를 문서화하면 운영 관점 포트폴리오로 확장하기 좋습니다.
