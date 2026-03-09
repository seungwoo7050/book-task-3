# Problem Framing

## Objective

acknowledged write를 잃지 않도록 append-only WAL을 구현하고, corruption이나 partial write가 있을 때 보수적으로 replay를 중단하는 recovery path를 만든다.

## Requirements

- PUT/DELETE는 MemTable 반영 전에 WAL에 먼저 기록되어야 한다.
- record는 CRC32, type, key length, value length, payload를 포함해야 한다.
- replay는 첫 손상 레코드에서 멈추고 그 뒤는 버려야 한다.
- flush 후에는 기존 WAL을 제거하고 새 WAL을 열어야 한다.

## Source Provenance

- 원본 문제: `legacy/storage-engine/wal-recovery/problem/README.md`
- 원본 solution 참고: `legacy/storage-engine/wal-recovery/solve/solution/wal.js`
- 확장 이유: WAL 단독 구현에 더해 durable store integration과 post-flush rotation을 함께 검증하기 위해서다.

