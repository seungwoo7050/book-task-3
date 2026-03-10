# 04 Buffer Pool

disk-backed page를 메모리에 캐시하고 pin count와 dirty write-back 정책을 포함한 buffer pool manager를 구현합니다.

## 이 프로젝트에서 배우는 것

- 고정 크기 page를 메모리에 캐시하는 기본 구조를 익힙니다.
- pin/unpin이 eviction 가능 여부를 어떻게 바꾸는지 이해합니다.
- dirty page를 flush하거나 write-back하는 시점을 설계합니다.

## 먼저 알고 있으면 좋은 것

- 기본 파일 I/O와 page 개념을 알고 있으면 좋습니다.
- cache replacement 정책의 기초를 알고 있으면 읽기 쉽습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `src/`와 `tests/`를 함께 읽고, 마지막에 패키지 entry point를 실행해 전체 흐름을 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `src/buffer_pool/`, `tests/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd python/database-internals/04-buffer-pool
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U pytest
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m buffer_pool
```

## 구현에서 집중할 포인트

- cache hit와 miss 경로가 모두 pin count를 올바르게 갱신하는지 확인합니다.
- pinned page가 eviction 후보에서 확실히 제외되는지 봅니다.
- dirty flush와 page fetch가 같은 file/page identity를 공유하는지 확인합니다.

## 포트폴리오로 발전시키려면

- Clock replacer나 async flush worker를 추가하면 시스템 설계 폭이 넓어집니다.
- cache hit ratio, flush 횟수, pin 대기 같은 지표를 넣으면 운영 관점 이야기가 생깁니다.
