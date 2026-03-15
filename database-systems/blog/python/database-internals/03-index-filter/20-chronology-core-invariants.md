# 20 핵심 invariant 붙잡기: bloom reject와 bounded block scan이 어디서 잠기는가

이 슬롯의 코드는 길지 않지만, lookup 비용을 줄이는 핵심 단계가 꽤 잘 분리돼 있다. `BloomFilter`, `SparseIndex`, `SSTable.write/load/get_with_stats()`만 따라가면, 왜 miss는 0 bytes read로 끝나고 hit는 작은 범위만 읽게 되는지 거의 다 설명된다.

## Phase 2-1. Bloom filter는 "빨리 아니다"를 말하는 역할만 맡는다

`BloomFilter` 구현을 다시 보면 역할이 분명하다. `add()`는 bit positions를 켜고, `might_contain()`은 어느 한 비트라도 꺼져 있으면 즉시 `False`를 준다. 즉 Bloom filter는 positive를 확정하지 않는다. negative를 빨리 확정하는 데만 집중한다.

중요한 건 구현 세부다. 개념 문서는 MurmurHash3 식의 설명을 하고 있지만, 실제 `_hash_value()`는 `sha256(seed:key)`의 앞 8바이트를 정수로 읽고, `positions()`는 두 hash를 이용한 double hashing으로 k개 위치를 만든다. 그래서 source 기준으로 보면 이 프로젝트는 "MurmurHash3 구현"이 아니라 "SHA-256 기반 double hashing Bloom filter"다.

테스트도 이 해석과 맞는다.

- false negative는 허용하지 않는다
- false positive rate는 목표 1%보다 조금 느슨하게 `<= 3%`까지 허용한다

즉 엄격한 최적 해시 구현보다, 학습용 bit budget 감각과 negative fast-path를 먼저 보여 주는 쪽에 가깝다.

## Phase 2-2. Sparse index는 full scan을 작은 block 후보로 줄인다

`SparseIndex.build()`는 모든 key-offset를 저장하지 않고, `block_size`마다 한 개씩만 남긴다. `find_block()`은 `largest indexed key <= target`을 이진 탐색으로 찾고, 그 block의 시작/끝 offset만 반환한다.

이것만 보면 단순해 보이지만, 역할은 분명하다. Bloom filter가 miss 후보를 먼저 잘라내고 나면, sparse index는 positive candidate의 scan 범위를 data section 전체가 아니라 특정 byte window로 줄인다. 결국 filter와 index는 경쟁 관계가 아니라 두 단계 파이프다.

보조 재실행에서도 이 흐름이 숫자로 드러났다.

```text
footer_magic b'SIF1' data_size 1024 bloom_offset 1024 index_offset 1110
missing LookupStats(bloom_rejected=True, bytes_read=0, block_range=(0, 0))
hit LookupStats(bloom_rejected=False, bytes_read=128, block_range=(256, 384))
```

즉 missing key는 아예 disk block을 읽지 않았고, hit key는 data section 1024바이트 전체가 아니라 128바이트 구간만 읽었다.

## Phase 2-3. `SSTable.write()`는 data/filter/index/footer를 한 파일 안에 배치한다

이 프로젝트의 SSTable은 네 구역으로 파일을 쓴다.

1. data section
2. bloom bytes
3. sparse index bytes
4. footer

`write()`는 records를 먼저 encoded data section으로 직렬화하고, 같은 key stream으로 Bloom filter와 sparse index를 만들고, 마지막에 `FOOTER_MAGIC + bloom/index offsets + block_size`를 붙인다. 그래서 `load()`는 파일 맨 끝 40바이트만 읽으면 filter와 index의 위치를 다시 복원할 수 있다.

이 구조가 중요한 이유는 lookup 때 metadata read를 다시 설계할 수 있기 때문이다. data section 전체를 미리 읽지 않고도, footer를 기준으로 filter와 index를 찾아서 negative fast-path와 bounded scan을 구성할 수 있다.

## Phase 2-4. `get_with_stats()`가 비용 절감 경로를 직접 노출한다

이 프로젝트에서 가장 좋은 함수 이름은 `get_with_stats()`다. 단순 `get()`보다 훨씬 정직하다. 이 함수는 value/ok뿐 아니라 `LookupStats`도 같이 돌려준다.

경로는 정확히 세 단계다.

1. filter가 miss면 `bloom_rejected=True`, `bytes_read=0`
2. filter가 hit면 sparse index로 `(start, end)` block range를 계산
3. 해당 block만 읽어서 decode하다가 key를 찾거나 key가 target을 지나치면 종료

즉 이 프로젝트의 진짜 산출물은 value 자체보다 "왜 이만큼만 읽고 끝났는가"를 설명 가능한 stats에 가깝다. 그래서 demo도 value보다 `bytes_read`를 같이 보여 준다.

한 가지 현재 seam도 있다. `get_with_stats()`의 네 번째 반환값은 항상 `None`이다. 앞으로 trace나 debug payload를 붙일 여지를 남겨 둔 셈이지만, 지금 단계에선 아직 사용되지 않는 placeholder다.
