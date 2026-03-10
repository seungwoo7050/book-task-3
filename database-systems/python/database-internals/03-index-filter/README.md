# 03 Index Filter

Bloom filter와 sparse index를 붙여 point lookup이 전체 SSTable 스캔으로 떨어지지 않도록 만듭니다.

## 이 프로젝트에서 배우는 것

- Bloom filter가 negative lookup 비용을 어떻게 줄이는지 이해합니다.
- sparse index가 block scan 범위를 좁히는 방식을 익힙니다.
- footer metadata로 filter/index 위치를 복원하는 방법을 확인합니다.

## 먼저 알고 있으면 좋은 것

- SSTable layout과 point lookup 흐름을 알고 있으면 좋습니다.
- 확률 자료구조의 false positive 개념을 알면 읽기 쉽습니다.

## 추천 읽기 순서

1. `problem/README.md`로 문제 해석과 현재 범위를 먼저 확인합니다.
2. `docs/README.md`와 개념 노트를 읽어, 코드에 들어가기 전 핵심 용어를 맞춥니다.
3. `src/`와 `tests/`를 함께 읽고, 마지막에 패키지 entry point를 실행해 전체 흐름을 확인합니다.
4. `notion/README.md`와 `notion/01-approach-log.md`로 설계 판단과 학습 메모를 확인합니다.

## 구현 표면

- `problem/`: 현재 프로젝트 문제 해석과 제공 자료
- `docs/`: 개념 메모와 설명형 참고자료 목록
- `src/index_filter/`, `tests/`: 실제 구현과 검증 코드
- `notion/`: 현재 공개용 학습 노트
- `notion-archive/`: 이전 세대 문서 보관본

## 검증 명령

```bash
cd python/database-internals/03-index-filter
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -U pytest
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m index_filter
```

## 구현에서 집중할 포인트

- 없는 key가 filter 단계에서 조기에 탈락하는지 확인합니다.
- 있는 key일 때 scan 범위가 block 단위로 제한되는지 봅니다.
- filter/index 직렬화와 reopen 복원이 일관적인지 확인합니다.

## 포트폴리오로 발전시키려면

- false positive rate 실험과 bit budget 비교표를 추가하면 설계 감각을 드러내기 좋습니다.
- block cache와 range scan을 연결하면 읽기 최적화 이야기로 확장할 수 있습니다.
