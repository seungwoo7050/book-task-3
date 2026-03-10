# 학습 노트 안내

디스크 page를 메모리 frame으로 올려 재사용하는 buffer pool과, 그 위에서 eviction 순서를 정하는 LRU를 분리해 배우는 단계입니다.

## 이 노트를 읽기 전에 잡을 질문
- 같은 page를 여러 번 읽을 때 어떤 객체를 다시 써야 하고, 어떤 조건에서만 eviction을 허용해야 안전한가?
- 다음 단계 `05 MVCC`에 무엇을 넘기는가?

## 권장 읽기 순서
1. `../problem/README.md`로 요구와 범위를 먼저 확인합니다.
2. `../src/buffer_pool/core.py`, `../src/buffer_pool/core.py`, `../tests/test_buffer_pool.py`를 열어 실제 구현 표면을 먼저 잡습니다.
3. `../tests/`에서 이 프로젝트가 무엇을 보장하는지 확인합니다. 핵심 테스트는 `test_lru_basic_operations`, `test_lru_eviction_and_promotion`, `test_lru_ordering_and_delete`, `test_fetch_page_from_disk`입니다.
4. 데모 경로 `../src/buffer_pool/__main__.py`를 실행해 전체 흐름을 빠르게 눈으로 확인합니다.
5. 마지막으로 `./00-problem-framing.md`부터 `./04-knowledge-index.md`까지 읽으며 판단과 연결 지점을 정리합니다.

## 이번 노트가 담는 것
- `00-problem-framing.md`: 같은 page를 여러 번 읽을 때 어떤 객체를 다시 써야 하고, 어떤 조건에서만 eviction을 허용해야 안전한가?에 대한 범위와 성공 기준을 정리합니다.
- `01-approach-log.md`: eviction 정책과 page 상태를 분리한다, pin count를 eviction 금지 신호로 쓴다 같은 실제 구현 선택을 기록합니다.
- `02-debug-log.md`: cache hit인데 새 Page 객체를 만드는 경우, pin이 남아 있는데 eviction하는 경우처럼 다시 깨질 수 있는 지점을 모아 둡니다.
- `03-retrospective.md`: 이 단계에서 얻은 것, 남긴 단순화, 다음 확장 방향을 정리합니다.
- `04-knowledge-index.md`: 용어, 핵심 파일, 개념 문서, 검증 앵커를 빠르게 다시 찾는 인덱스입니다.

## 검증 앵커
- 테스트: `test_lru_basic_operations`, `test_lru_eviction_and_promotion`, `test_lru_ordering_and_delete`, `test_fetch_page_from_disk`
- 데모 경로: `../src/buffer_pool/__main__.py`
- 데모가 보여 주는 장면: Go 데모는 page 1을 읽어 앞부분 문자열을 출력합니다. Python 데모도 page id, pin count, prefix를 dict로 출력해 disk fetch와 cache state를 함께 보여 줍니다.
- 개념 문서: `../docs/concepts/lru-eviction.md`, `../docs/concepts/pin-and-dirty.md`

- 이전 장문 기록은 `../notion-archive/`에 보존돼 있습니다.
