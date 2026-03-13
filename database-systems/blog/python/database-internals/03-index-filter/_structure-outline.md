# 03 Index Filter — Structure Outline

최종 시리즈는 chronology를 매끈하게 재배열하지 않고, 범위 파악 -> 핵심 invariant -> 재검증과 경계의 순서를 유지한다.

## Planned Files

- `00-series-map.md`: 프로젝트 질문, 읽는 순서, source-of-truth 파일, 재검증 명령을 잡는 지도
- `10-chronology-scope-and-surface.md`: 파일 구조와 테스트 이름을 근거로 처음 가설이 바뀌는 구간
- `20-chronology-core-invariants.md`: `BloomFilter`와 `_hash_value`가 실제로 invariant를 고정하는 구간
- `30-chronology-verification-and-boundaries.md`: `go test`/`pytest`와 demo 출력으로 경계를 확정하는 구간

## Article Goals

1. `10-chronology-scope-and-surface.md`
   범위를 `tests/`와 README에서 어떻게 다시 좁혔는지 보여 준다.
   코드 앵커: `test_bloom_filter_has_no_false_negatives`, `BloomFilter`
   CLI: `find src tests -type f | sort`, `rg -n "^def test_" tests`

2. `20-chronology-core-invariants.md`
   핵심 invariant가 `BloomFilter`와 `_hash_value` 사이에서 어떻게 고정되는지 보여 준다.
   코드 앵커: `BloomFilter`, `_hash_value`
   CLI: `rg -n "^(class|def) " src`, `rg -n "BloomFilter|_hash_value" src`

3. `30-chronology-verification-and-boundaries.md`
   테스트와 demo를 모두 남겨, pass 신호와 공개 표면을 구분해 설명한다.
   코드 앵커: `test_sstable_bloom_reject_and_bounded_scan`, `__main__.py`
   CLI: PYTHONPATH=src .venv/bin/python -m pytest; PYTHONPATH=src .venv/bin/python -m index_filter
