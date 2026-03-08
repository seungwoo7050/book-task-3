# Flush Lifecycle

- active MemTable은 write를 받는 유일한 구조다.
- threshold를 넘으면 active MemTable이 immutable로 바뀌고, 새 empty MemTable이 즉시 write를 받는다.
- immutable snapshot을 SSTable로 내린 뒤 table registry의 newest 위치에 등록한다.
- 이 프로젝트는 flush를 동기 처리하지만, 상태 분리는 나중의 async flush 모델과 같은 개념을 유지한다.

