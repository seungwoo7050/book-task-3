# 문제 정의

append-only distributed commit log의 핵심인 store, index, segment, log abstraction을 구현한다.

## 성공 기준

- length-prefixed record store를 구현한다.
- offset -> position을 매핑하는 fixed-width mmap index를 구현한다.
- segment가 base offset과 next offset을 관리하며 full 상태를 판정한다.
- log가 active segment rotation과 read/append/reset을 지원한다.
- 파일 정리와 reopen 시나리오를 테스트로 검증한다.

## 제공 자료와 출처

- legacy `02-distributed-system/05-distributed-log` 문제를 한국어 canonical 형태로 다시 정리한 문서다.
- 원문 요구사항과 replication bonus는 provenance로만 유지한다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `make -C problem test`
- `make -C problem bench`

## 제외 범위

- replication layer
- networked consensus
