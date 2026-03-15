# 04 WAL Recovery

## 이 랩의 실제 초점

이 프로젝트는 durability를 말하지만, 그 핵심은 추상적 "영속성"이 아니라 아주 구체적인 write ordering과 replay policy에 있다. `Put`과 `Delete`는 memtable보다 WAL에 먼저 append돼야 하고, reopen 시에는 WAL record를 다시 읽어 memtable을 복원해야 하며, flush 뒤에는 기존 WAL을 비우고 새 active WAL로 회전해야 한다. 손상된 레코드를 만났을 때는 그 지점에서 멈추고 이후는 버린다.

즉 이 랩은 LSM store에 durability를 얹는 첫 단계다. group commit이나 fsync batching은 아직 없지만, append-before-apply와 stop-on-corruption이라는 핵심 계약은 분명히 드러난다.

이번 시리즈는 기존 blog를 입력 근거로 쓰지 않고 [`problem/README.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/problem/README.md), [`store.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/internal/store/store.go), [`wal.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/internal/wal/wal.go), [`wal_test.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/tests/wal_test.go), [`main.go`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/04-wal-recovery/cmd/wal-recovery/main.go), 그리고 2026-03-14 재실행 결과만으로 다시 썼다.

## 이번에 붙드는 질문

- append-before-apply는 코드에서 정확히 어디서 보장되는가
- WAL record는 어떤 header와 checksum으로 구성되는가
- replay는 언제 멈추고 무엇을 버리는가
- flush 이후 WAL rotation과 reopen recovery는 어떤 순서로 이어지는가

## 문서 지도

- [10-chronology-scope-and-surface.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/04-wal-recovery/10-chronology-scope-and-surface.md): 문제 범위, write/reopen 표면, demo 결과를 시간순으로 정리한다.
- [20-chronology-core-invariants.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/04-wal-recovery/20-chronology-core-invariants.md): WAL record format, append-before-apply, stop-on-corruption, WAL rotation을 소스 기준으로 해부한다.
- [30-chronology-verification-and-boundaries.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/04-wal-recovery/30-chronology-verification-and-boundaries.md): go test와 demo, 추가 재실행을 바탕으로 현재 검증 범위와 한계를 정리한다.
- [_evidence-ledger.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/04-wal-recovery/_evidence-ledger.md): 근거 파일과 재실행 명령, 관찰값을 남긴다.
- [_structure-outline.md](/Users/woopinbell/work/book-task-3/database-systems/blog/go/database-internals/04-wal-recovery/_structure-outline.md): 문서 구조 선택 이유와 버린 접근을 적는다.

## 지금 기준의 결론

이 랩은 Go 저장 엔진 트랙에서 durability story의 출발점이다. WAL append, replay, corruption stop policy, flush 뒤 active WAL rotation은 선명하다. 반대로 group commit, multi-writer, distributed recovery는 아직 없다.
