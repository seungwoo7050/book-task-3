# Read Path

- 먼저 active MemTable을 본다.
- flush 중이면 immutable MemTable을 본다.
- 그다음 newest SSTable부터 oldest SSTable 순서로 본다.
- tombstone이 발견되면 lookup은 즉시 "삭제됨"으로 종료해야 한다.

