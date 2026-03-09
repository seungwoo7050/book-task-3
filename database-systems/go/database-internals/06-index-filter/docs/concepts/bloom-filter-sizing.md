# Bloom Filter Sizing

Bloom filter는 false negative가 없어야 하고, false positive는 허용 가능한 수준으로만 남아야 한다. 이 프로젝트는 레거시와 같은 식을 사용한다.

- `m = -(n * ln(p)) / (ln2)^2`
- `k = (m / n) * ln2`

여기서 `n`은 예상 item 수, `p`는 목표 false positive rate다. 실제 구현에서는 bit array 길이를 byte 단위로 올림하고, MurmurHash3 두 개로 double hashing을 만들어 `k`개의 position을 유도한다.
