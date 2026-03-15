# 30 다시 돌려 보기: filter와 index가 실제로 얼마나 덜 읽게 만드는가

마지막으로 확인할 건 theory가 아니라 숫자다. Bloom filter와 sparse index는 설명만으로는 쉽게 과장된다. 실제로 몇 바이트를 읽고, 어떤 경우에 0바이트로 끝나는지 다시 봐야 현재 경계가 보인다.

## Phase 3-1. pytest는 정확도보다 비용 감소 계약을 잡는다

이번 재실행에서 pytest는 `4 passed, 1 warning in 0.04s`였다. 경고는 앞선 두 슬롯과 같은 `pytest_asyncio` deprecation이라 프로젝트 핵심과는 무관했다.

테스트가 잠그는 건 네 가지다.

- Bloom filter는 false negative가 없어야 한다
- false positive rate는 3% 이하여야 한다
- sparse index는 기대 block range를 찾아야 한다
- SSTable lookup은 bloom reject와 bounded scan을 둘 다 드러내야 한다

즉 이 프로젝트의 검증 축은 "정확히 읽었는가"보다 "덜 읽으면서도 맞게 찾았는가"다.

## Phase 3-2. demo는 bounded scan의 감각을 한 줄로 보여 준다

demo entry point를 다시 돌리면 이런 출력이 나온다.

```bash
cd /Users/woopinbell/work/book-task-3/database-systems/python/database-internals/projects/03-index-filter
PYTHONPATH=src python3 -m index_filter
```

```text
{'found': True, 'value': 'value-k023', 'bytes_read': 176}
```

이 한 줄에서 중요한 건 `bytes_read`다. 전체 data section을 다 읽지 않았다는 감각을 가장 빠르게 보여 준다. 이 demo는 false positive rate나 footer offset까지는 드러내지 않지만, lookup 최적화의 결과를 밖으로 노출하는 최소 표면 역할은 충분히 한다.

## Phase 3-3. 보조 재실행이 footer와 block range를 더 선명하게 보여 줬다

이번 Todo에서는 demo 외에도 한 번 더 파일을 직접 확인했다.

- footer magic: `SIF1`
- data size: `1024`
- bloom offset: `1024`
- index offset: `1110`
- missing key stats: `bloom_rejected=True`, `bytes_read=0`
- hit key stats: `bytes_read=128`, `block_range=(256, 384)`

이 숫자들이 의미하는 건 명확하다.

1. metadata는 footer를 통해 복원된다.
2. miss는 filter에서 즉시 잘리면 실제 data read가 없다.
3. hit여도 data section 전체가 아니라 선택된 block만 읽는다.

즉 이 슬롯은 "index가 있다"가 아니라 "negative path와 positive path가 서로 다른 비용 절감 경로를 가진다"는 사실을 파일 구조 수준으로 보여 준다.

## Phase 3-4. 지금 상태에서 비워 둔 것

현재 구현은 교육용으로 충분히 선명하지만, production read path라고 보긴 어렵다.

- hash 함수는 단순 SHA-256 기반이고, docs 설명과 완전히 같지 않다.
- false positive rate는 deterministic upper bound가 아니라 test-sampled empirical bound다.
- range query 최적화가 없다.
- block cache가 없다.
- `get_with_stats()`의 네 번째 반환값은 아직 항상 `None`이다.

그래도 이 프로젝트가 중요한 이유는 분명하다. 앞선 two slots가 "어떻게 쓰고 보존할 것인가"를 고정했다면, 이 슬롯은 처음으로 "읽기 비용을 어떻게 줄일 것인가"를 byte-level stats와 함께 보여 주기 때문이다. 이후 buffer pool이나 더 복잡한 read path로 넘어갈 때 필요한 감각이 바로 여기서 생긴다.
