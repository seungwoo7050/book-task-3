# Dirty Pages And Writeback

## dirty bit가 필요한 이유

page replacement는 단순히 “무엇을 뺄까”만이 아니라 “무엇을 디스크에 다시 써야 하나”도 함께 결정한다. 읽기 전용 page라면 바로 버릴 수 있지만, write가 있었던 page는 write-back 비용이 따라온다.

## 이 프로젝트의 단순화

- `W <page>` 접근이 한 번이라도 있으면 그 frame은 dirty로 표시한다.
- dirty frame이 eviction되면 `dirty_evictions`를 1 올린다.
- 실제 disk latency나 asynchronous flush는 넣지 않는다.

이 단순화 덕분에 hit/fault 계산기와 “write-back cost를 의식하는 replacement model”의 차이를 작은 trace로 보여 줄 수 있다.
