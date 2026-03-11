# 없는 키는 빠르게 거절하고, 있는 키는 좁은 범위만 읽기

## SSTable 조회의 비효율

02번에서 만든 SSTable은 모든 키에 대해 인덱스를 가지고 있었다. 파일에 1000개의 레코드가 있으면, 인덱스에도 1000개의 `(key, offset)` 쌍이 있었다.

이 방식의 문제 두 가지:
1. **인덱스가 크다**: 레코드 수에 비례해서 인덱스가 커진다. 메모리에 올리는 비용이 만만치 않다.
2. **없는 키도 확인해야 한다**: 이 SSTable에 없는 키라도, 인덱스를 이진 탐색해봐야 "없다"는 걸 알 수 있다.

이 프로젝트는 두 가지 장치로 이 문제를 해결한다:
- **Bloom filter**: 없는 키를 O(1)에 거절한다.
- **Sparse index**: 매 N번째 키만 인덱스에 넣어서 인덱스 크기를 1/N로 줄인다.

## Bloom filter: 확률적 집합 멤버십 테스트

Bloom filter는 "이 키가 이 집합에 있을 수 있는가?"를 답하는 자료구조다.

**특성**:
- "없다"고 하면 **확실히 없다** (false negative 없음)
- "있을 수 있다"고 하면 **실제로는 없을 수도 있다** (false positive 존재)

내부 구조는 비트 배열이다. 키를 추가할 때 k개의 해시 함수로 k개의 위치를 계산해서 해당 비트를 1로 설정한다. 조회할 때도 같은 k개 위치를 확인해서, 하나라도 0이면 "확실히 없다"고 판정한다.

### 파라미터 결정

비트 배열 크기 $m$과 해시 함수 수 $k$는 원하는 false positive rate $p$와 예상 키 수 $n$으로 결정한다:

$$m = -\frac{n \ln p}{(\ln 2)^2}$$
$$k = \frac{m}{n} \ln 2$$

이 프로젝트에서는 false positive rate 1%를 목표로 했다.

### 해시 함수

k개의 독립적인 해시 함수 대신, **double hashing** 기법을 사용한다:
- $h_1 = \text{MurmurHash3}(key, seed=0)$
- $h_2 = \text{MurmurHash3}(key, seed=42)$
- $i$번째 위치 = $(h_1 + i \cdot h_2) \mod m$

이렇게 하면 해시 함수를 두 번만 호출하고도 k개의 분산된 위치를 얻을 수 있다. MurmurHash3는 `shared/hash` 패키지에 구현되어 있다.

### 직렬화

Bloom filter를 SSTable 파일 안에 포함시키려면 직렬화가 필요하다.
포맷: `[bitCount: 4B][hashFunctions: 4B][bits...]`. 8바이트 헤더에 비트 배열을 그대로 붙인다.

## Sparse index: 모든 키를 인덱스하는 대신

02번의 dense index는 모든 키를 기록했다. Sparse index는 매 `blockSize`번째 키만 기록한다.

예를 들어 blockSize=16이면, 1000개 레코드 중 63개(≈1000/16)만 인덱스에 들어간다. 인덱스 크기가 약 1/16로 줄어든다.

조회 시에는 sparse index에서 이진 탐색으로 **키가 속할 수 있는 블록 범위**를 찾는다. 해당 블록(시작 offset부터 다음 인덱스 엔트리의 offset까지)만 읽어서 순차 스캔한다.

블록 범위를 찾는 규칙:
- 키가 첫 인덱스 엔트리보다 작으면 → 이 SSTable에 없다
- 그렇지 않으면 → key 이하인 가장 큰 인덱스 엔트리의 블록. 블록 끝은 다음 엔트리의 offset (마지막 블록이면 Data Section 끝)

## 확장된 SSTable 포맷

02번과 달라진 파일 레이아웃:

```
[ Data Section ][ Bloom Filter ][ Sparse Index ][ Footer (40 bytes) ]
```

Footer 40바이트:
- Magic: `SIF1` (4B)
- Bloom offset, size (각 8B)
- Index offset, size (각 8B)
- Block size (4B)

Magic 바이트는 이 포맷이 index-filter 포맷임을 식별하는 용도다. 02번의 8바이트 footer와 혼동되지 않게 한다.

## 조회 경로: filter → index → block scan

1. **Bloom filter 검사**: `MightContain(key)`가 false면 즉시 "없다"로 반환. 디스크 I/O 없음.
2. **Sparse index 검사**: `FindBlock(key)`으로 블록 범위를 찾는다.
3. **Block scan**: 해당 범위의 바이트를 읽어서 레코드를 순차 디코딩. 키를 찾거나 키보다 큰 레코드를 만나면 중단.

`GetWithStats` 메서드는 이 과정의 통계를 반환한다: `BloomRejected` 여부, 읽은 바이트 수, 블록 범위. 이 통계로 filter와 index가 실제로 I/O를 줄이는지 검증할 수 있다.

## 테스트로 확인한 것

- **Bloom filter 단독**: 추가한 키는 항상 MightContain=true, 없는 키의 false positive rate가 상한 이내
- **Sparse index 단독**: blockSize 기반 블록 범위 계산, 범위 밖 키 거절
- **SSTable 통합**: Write → Load → Get round-trip, bloom rejection 확인
- **Serialization round-trip**: filter와 index의 직렬화→역직렬화

## 돌아보며

이 프로젝트에서 가장 인상적이었던 것은 **확률 자료구조의 실용성**이다.

Bloom filter는 100% 정확하지 않다. false positive가 있다. 하지만 "없는 키를 빠르게 거절"하는 용도에서는 99%의 정확도면 충분하다. 1%의 오판은 그냥 블록을 한 번 더 읽으면 되니까.

sparse index도 마찬가지다. 정확한 offset을 못 찾는 대신 블록 단위로 좁혀준다. 정확하지 않아도, 범위를 충분히 줄여주면 실용적이다.

다음 프로젝트(07-buffer-pool)에서는 이 SSTable 블록을 메모리에 캐싱하는 buffer pool을 다룬다.
