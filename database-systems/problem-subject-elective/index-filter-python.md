# index-filter-python 문제지

## 왜 중요한가

Bloom filter를 직렬화·복원할 수 있어야 합니다. 정렬된 key-offset 스트림에서 sparse index를 생성해야 합니다. footer metadata를 읽어 filter와 index 위치를 복원해야 합니다. lookup 시 bloom reject와 bounded block scan이 둘 다 드러나야 합니다.

## 목표

시작 위치의 구현을 완성해 Bloom filter를 직렬화·복원할 수 있어야 합니다, 정렬된 key-offset 스트림에서 sparse index를 생성해야 합니다, footer metadata를 읽어 filter와 index 위치를 복원해야 합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../python/database-internals/projects/03-index-filter/src/index_filter/__init__.py`
- `../python/database-internals/projects/03-index-filter/src/index_filter/__main__.py`
- `../python/database-internals/projects/03-index-filter/src/index_filter/table.py`
- `../python/database-internals/projects/03-index-filter/tests/test_index_filter.py`
- `../python/database-internals/projects/03-index-filter/pyproject.toml`

## starter code / 입력 계약

- `../python/database-internals/projects/03-index-filter/src/index_filter/__init__.py`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- Bloom filter를 직렬화·복원할 수 있어야 합니다.
- 정렬된 key-offset 스트림에서 sparse index를 생성해야 합니다.
- footer metadata를 읽어 filter와 index 위치를 복원해야 합니다.
- lookup 시 bloom reject와 bounded block scan이 둘 다 드러나야 합니다.

## 제외 범위

- 같은 주제의 다른 runtime 구현을 섞어 읽지 않는다.

## 성공 체크리스트

- 핵심 흐름은 `_hash_value`와 `encode_record`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_bloom_filter_has_no_false_negatives`와 `test_bloom_filter_false_positive_rate_is_bounded`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/03-index-filter && PYTHONPATH=src python3 -m pytest`가 통과한다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/03-index-filter && PYTHONPATH=src python3 -m pytest
```

- 이 검증 명령을 직접 실행하려면 현재 셸에 `pytest`가 설치돼 있어야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`index-filter-python_answer.md`](index-filter-python_answer.md)에서 확인한다.
