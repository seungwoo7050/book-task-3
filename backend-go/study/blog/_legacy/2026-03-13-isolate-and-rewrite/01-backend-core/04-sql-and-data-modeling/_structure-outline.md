# 04 SQL And Data Modeling Structure Outline

이 문서는 chronology ledger를 바탕으로 최종 blog를 어떤 순서로 전개할지 먼저 고정한 설계 메모다. 기존 `blog/` 초안은 입력에서 제외했고, 실제 코드, README, docs, 테스트, CLI만을 근거로 삼는다.

## Planned Files

- `00-series-map.md`: 프로젝트 범위, source-of-truth, 읽는 순서를 잡는 진입 문서
- `01-evidence-ledger.md`: 파일, 함수, CLI 단위 chronology를 거칠게 복원한 근거 문서
- `10-2026-03-13-reconstructed-development-log.md`: 구현 순서와 판단 전환점을 세션 흐름으로 다시 쓴 최종 blog

## Final Blog Flow

- 도입: README 한 줄 요약과 이번 재검증 범위를 붙여 글의 위치를 먼저 밝힌다.
- 구현 순서 요약: Phase 1 -> Phase 2 -> Phase 3 순서를 미리 보여 준다.
- 세션형 chronology: 각 phase에서 당시 목표, 가설, 조치, 코드 앵커, 검증 신호를 순서대로 다시 적는다.
- CLI로 닫는 구간: 현재 저장소에서 다시 실행한 명령과 excerpt를 붙여 README 계약이 아직 살아 있는지 확인한다.
- 남은 질문: 개념 축과 다음 실험 지점을 남긴다.

## Section Plan

### 1. Phase 1 - ApplySchema와 Seed로 데이터 모델의 바닥을 먼저 깐다

- 목표: ApplySchema와 Seed로 데이터 모델의 바닥을 먼저 깐다
- 변경 단위: `solution/go/catalog/catalog.go`의 `ApplySchema`
- 핵심 가설: `ApplySchema`를 먼저 고정하면 I/O보다 데이터 규칙을 더 선명하게 설명할 수 있다고 봤다.
- 반드시 넣을 코드 앵커: `ApplySchema`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `alice owns 2 x potion`였다.
- 새로 배운 것 섹션 포인트: `players`, `items`, `inventory` 분리는 다대다 관계를 명시적으로 드러낸다.
- 다음 섹션 연결 문장: Purchase와 schemawalk CLI로 SQL 경로를 노출한다
### 2. Phase 2 - Purchase와 schemawalk CLI로 SQL 경로를 노출한다

- 목표: Purchase와 schemawalk CLI로 SQL 경로를 노출한다
- 변경 단위: `solution/go/catalog/catalog.go`의 `Purchase`
- 핵심 가설: `Purchase`를 중심에 두면 demo entrypoint는 얇은 연결층으로 남길 수 있다고 판단했다.
- 반드시 넣을 코드 앵커: `Purchase`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `ok  	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/catalog	(cached)`였다.
- 새로 배운 것 섹션 포인트: SQLite in-memory는 입문에는 좋지만 실제 운영 DB의 락/격리 수준과는 다르다.
- 다음 섹션 연결 문장: catalog_test로 재고 차감과 rollback 계약을 잠근다
### 3. Phase 3 - catalog_test로 재고 차감과 rollback 계약을 잠근다

- 목표: catalog_test로 재고 차감과 rollback 계약을 잠근다
- 변경 단위: `solution/go/catalog/catalog_test.go`의 `TestPurchase`
- 핵심 가설: 테스트 이름 `TestPurchase`처럼 계약을 먼저 못 박아야 구현이 흔들리지 않는다고 봤다.
- 반드시 넣을 코드 앵커: `TestPurchase`
- 반드시 넣을 검증 신호: `exit 0`; 최근 재실행 excerpt의 첫 줄은 `ok  	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/catalog	(cached)`였다.
- 새로 배운 것 섹션 포인트: `quantity <= 0` 같은 제약을 SQL과 애플리케이션 양쪽에서 동시에 생각하지 않으면 빈틈이 생긴다.
- 다음 섹션 연결 문장: 마지막엔 현재 저장소에서 다시 돌린 CLI와 남은 질문으로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/04-sql-and-data-modeling && cd solution/go && go run ./cmd/schemawalk)
```

```text
alice owns 2 x potion
```

```bash
(cd /Users/woopinbell/work/book-task-3/backend-go/study/01-backend-core/04-sql-and-data-modeling && cd solution/go && go test ./...)
```

```text
ok  	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/catalog	(cached)
?   	github.com/woopinbell/go-backend/study/01-backend-core/04-sql-and-data-modeling/cmd/schemawalk	[no test files]
```
