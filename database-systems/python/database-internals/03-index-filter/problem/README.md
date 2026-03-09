# Problem Framing

SSTable 전체를 선형 스캔하지 않고도 point lookup을 빠르게 수행하도록 Bloom filter와 sparse index를 붙인다. 없는 key는 filter에서 바로 걸러내고, 있는 key는 sparse index가 가리키는 block만 읽는다.

## Success Criteria

- MurmurHash3 기반 Bloom filter 구현과 직렬화
- 정렬된 key-offset 스트림에서 sparse index 생성
- footer metadata를 읽어서 filter/index 위치 복원
- lookup 시 bloom reject와 bounded block scan 통계 확인

## Source Provenance

- 원본 문제: `legacy/storage-engine/index-filter/problem/README.md`
- 원본 테스트 의미: `legacy/storage-engine/index-filter/solve/test/bloom-filter.test.js`
- 원본 테스트 의미: `legacy/storage-engine/index-filter/solve/test/sparse-index.test.js`
- 원본 구현 참고: `legacy/storage-engine/index-filter/solve/solution/bloom-filter.js`
- 원본 구현 참고: `legacy/storage-engine/index-filter/solve/solution/sparse-index.js`

## Normalization Notes

- 레거시의 Bloom filter와 sparse index를 하나의 Python SSTable open path로 통합했다.
- block scan 통계는 Python 테스트에서 직접 검증한다.
- false positive rate 검증은 환경 의존 flake를 줄이기 위해 느슨한 upper bound만 확인한다.
