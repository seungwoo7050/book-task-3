# 10 범위를 다시 좁히기: 이 슬롯의 목적은 정확도가 아니라 읽기 비용 경계다

처음엔 이 프로젝트를 Bloom filter 구현 연습처럼 보기 쉬웠다. 그런데 문제 정의와 테스트를 다시 훑어 보니, 실제 초점은 더 운영적이었다. "정확히 찾는가?"보다 "miss와 hit에서 각각 얼마나 적게 읽는가?"가 진짜 중심이었다.

## Phase 1. 테스트가 이미 두 종류의 비용 절감을 나눠 놓는다

`tests/test_index_filter.py`를 다시 보면 네 테스트가 정확히 두 축으로 나뉜다.

- Bloom filter 자체의 no false negative / bounded false positive rate
- sparse index + SSTable lookup이 실제로 bounded scan을 만드는가

특히 `test_sstable_bloom_reject_and_bounded_scan`이 중요했다. 이 테스트는 missing key에서 `stats.bloom_rejected is True`와 `stats.bytes_read == 0`을 요구하고, hit에서는 `0 < stats.bytes_read < table.data_size`를 요구한다. 즉 이 슬롯의 핵심 질문은 "찾았나?"보다 "얼마나 덜 읽었나?"다.

이번 재실행:

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/03-index-filter
PYTHONPATH=src python3 -m pytest
```

결과:

```text
4 passed, 1 warning in 0.04s
```

## Phase 2. 문제 정의와 docs가 말하는 것보다 source가 더 구체적이다

`problem/README.md`와 `docs/concepts/*`는 Bloom filter 직렬화, sparse index 생성, footer metadata 복원을 말한다. 그런데 source를 열어 보면 구현이 더 구체적이다.

- footer magic은 `SIF1`
- footer 길이는 magic 4바이트 + offset/size/block_size 36바이트, 총 40바이트
- miss는 Bloom filter에서 바로 끝나면 disk read가 0
- hit는 sparse index가 고른 block range만 읽고 그 안에서 decode를 멈춘다

또 하나 흥미로운 차이도 있다. 개념 문서는 MurmurHash3 계열 설명을 하지만, 실제 구현 `_hash_value()`는 SHA-256 digest 앞 8바이트를 써서 double hashing을 만든다. 즉 이 프로젝트의 진짜 contract는 개념 문서보다 source에 더 가깝다.

이 범위 재설정이 중요하다. 이 슬롯은 theoretical Bloom filter 강의가 아니라, 실제 SSTable file layout 안에서 filter와 index가 어떤 byte-saving 경로를 만드는지 보여 주는 프로젝트다.
