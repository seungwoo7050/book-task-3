# 접근 기록

## 읽기 순서 제안
1. `../problem/README.md`에서 요구와 현재 재구성 범위를 먼저 확인합니다.
2. 구현 핵심 파일을 열어 어떤 타입과 함수가 중심인지 확인합니다.
3. `../tests/`를 읽어 이 프로젝트가 실제로 고정한 계약을 확인합니다.
4. 데모를 실행해 테스트가 말하는 계약이 출력으로도 드러나는지 봅니다.
5. 마지막에 개념 문서를 읽으며 용어와 설계 판단을 정리합니다.

## 코드가 택한 분해 방식
### eviction 정책과 page 상태를 분리한다
- 관련 파일: `../internal/bufferpool/buffer_pool.go`, `../internal/lrucache/lru_cache.go`
- 판단: LRU는 “누가 가장 오래 안 쓰였는가”만 판단하고, buffer pool은 pin count와 dirty 상태를 본 뒤 eviction 가능 여부를 결정합니다.

### pin count를 eviction 금지 신호로 쓴다
- 관련 파일: `../internal/bufferpool/buffer_pool.go`
- 판단: page를 누군가 쓰는 동안은 오래 안 쓰였더라도 버리면 안 되므로 pin count를 분명한 경계로 둡니다.

### 작은 seed page 파일로 disk boundary를 드러낸다
- 관련 파일: `../tests/buffer_pool_test.go`
- 판단: 테스트가 직접 sample page file을 만들기 때문에 memory object만 보는 것이 아니라 실제 disk fetch 경계를 함께 볼 수 있습니다.

## 검증 명령
```bash
cd go/database-internals/07-buffer-pool
go test ./...
go run ./cmd/buffer-pool
```

## 포트폴리오 설명으로 바꿀 때 남길 장면
- cache hit에서 같은 page object를 재사용한다는 장면은 buffer pool 설명의 핵심입니다.
- pin count와 dirty flag를 분리한 이유를 설명하면 단순 캐시와의 차이가 드러납니다.
- LRU를 독립 모듈로 떼어 둔 구조는 “정책”과 “상태”를 분리했다는 좋은 설계 포인트입니다.
