# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### filter는 빠른 negative check, index는 scan 범위 축소로 역할을 나눈다
- 관련 파일: `../internal/bloomfilter/bloom_filter.go`, `../internal/sparseindex/sparse_index.go`
- 판단: bloom filter와 sparse index가 둘 다 “빨라진다”는 말을 하지만, 실제로는 하나는 읽지 않아도 되는 파일을 걸러내고 다른 하나는 읽어야 할 범위를 줄입니다.

### lookup 결과에 통계를 포함해 최적화 효과를 보이게 한다
- 관련 파일: `../internal/sstable/sstable.go`
- 판단: 단순히 값만 돌려주면 최적화가 작동했는지 보이지 않으므로 `LookupStats` 또는 동등한 구조를 같이 반환하게 했습니다.

### 논리 의미는 바꾸지 않고 read cost만 줄인다
- 관련 파일: `../internal/sstable/sstable.go`
- 판단: filter와 index를 붙여도 tombstone, missing, live value 의미는 이전 단계와 동일해야 합니다. 이 불변성이 있어야 최적화 단계가 안전합니다.

## 검증 명령
```bash
cd go/database-internals/projects/06-index-filter
go test ./...
go run ./cmd/index-filter
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- `bytes_read`와 `bloom_rejected`를 같이 보여 주면 최적화가 눈에 보입니다.
- filter와 index가 서로 다른 책임을 가진다는 설명은 단순 성능 튜닝이 아니라 구조적 분해를 보여 줍니다.
- Go와 Python 모두 같은 논리를 따르지만 표현이 조금 다르다는 비교도 좋은 설명 재료입니다.
