# index-filter-python 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 Bloom filter를 직렬화·복원할 수 있어야 합니다, 정렬된 key-offset 스트림에서 sparse index를 생성해야 합니다, footer metadata를 읽어 filter와 index 위치를 복원해야 합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `_hash_value`와 `encode_record`, `decode_record` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- Bloom filter를 직렬화·복원할 수 있어야 합니다.
- 정렬된 key-offset 스트림에서 sparse index를 생성해야 합니다.
- footer metadata를 읽어 filter와 index 위치를 복원해야 합니다.
- 첫 진입점은 `../python/database-internals/projects/03-index-filter/src/index_filter/__init__.py`이고, 여기서 `_hash_value`와 `encode_record` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../python/database-internals/projects/03-index-filter/src/index_filter/__init__.py`: 패키지 진입점과 공개 API 경계를 고정하는 파일이다.
- `../python/database-internals/projects/03-index-filter/src/index_filter/__main__.py`: CLI나 demo 실행 순서를 묶는 진입점 파일이다.
- `../python/database-internals/projects/03-index-filter/src/index_filter/table.py`: `_hash_value`, `encode_record`, `decode_record`, `LookupStats`가 핵심 흐름과 상태 전이를 묶는다.
- `../python/database-internals/projects/03-index-filter/tests/test_index_filter.py`: `test_bloom_filter_has_no_false_negatives`, `test_bloom_filter_false_positive_rate_is_bounded`, `test_sparse_index_finds_expected_block`가 통과 조건과 회귀 포인트를 잠근다.
- `../python/database-internals/projects/03-index-filter/pyproject.toml`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.
- `_hash_value` 구현은 `test_bloom_filter_has_no_false_negatives` 등이 잠근 입력 계약과 상태 전이를 그대로 만족해야 한다.
- 회귀 게이트는 `cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/03-index-filter && PYTHONPATH=src python3 -m pytest`이며, 핵심 상태 전이를 바꿀 때마다 중간 검증으로 다시 실행한다.
- `../python/database-internals/projects/03-index-filter/pyproject.toml`는 실행 루트와 모듈 경계를 고정해 검증이 어느 위치에서 돌아야 하는지 알려 준다.

## 정답을 재구성하는 절차

1. `../python/database-internals/projects/03-index-filter/src/index_filter/__init__.py`를 먼저 열어 입력과 상태 전이의 기준점을 잡는다.
2. `test_bloom_filter_has_no_false_negatives` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/03-index-filter && PYTHONPATH=src python3 -m pytest`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/03-index-filter && PYTHONPATH=src python3 -m pytest
```

- 상위 카탈로그나 보조 문서만 보고 구현을 추측하지 않고, 지금 열어 둔 source/test를 정답 근거로 고정한다.
- `test_bloom_filter_has_no_false_negatives`와 `test_bloom_filter_false_positive_rate_is_bounded`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/03-index-filter && PYTHONPATH=src python3 -m pytest`로 회귀를 조기에 잡는다.

## 소스 근거

- `../python/database-internals/projects/03-index-filter/src/index_filter/__init__.py`
- `../python/database-internals/projects/03-index-filter/src/index_filter/__main__.py`
- `../python/database-internals/projects/03-index-filter/src/index_filter/table.py`
- `../python/database-internals/projects/03-index-filter/tests/test_index_filter.py`
- `../python/database-internals/projects/03-index-filter/pyproject.toml`
