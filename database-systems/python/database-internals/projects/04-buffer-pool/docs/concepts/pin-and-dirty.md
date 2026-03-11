# Pin And Dirty

- pin count가 0보다 큰 page는 eviction 대상이 될 수 없다.
- dirty page는 메모리에서 사라지기 전에 디스크에 write-back 되어야 한다.
- `unpin(isDirty=true)`는 caller가 page를 수정했다는 신호다.

