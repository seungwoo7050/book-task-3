# 매번 디스크를 읽을 수는 없다 — Buffer Pool Manager

## 디스크 I/O 문제

지금까지 SSTable을 읽을 때마다 매번 파일을 열고, 원하는 위치를 읽고, 닫았다.
같은 페이지를 10번 읽으면 디스크 I/O도 10번이다.

데이터베이스 시스템에서는 이 문제를 **Buffer Pool**로 해결한다. 자주 쓰는 디스크 페이지를 메모리에 캐시하고, 같은 페이지를 다시 요청하면 캐시에서 돌려준다.

여기서 세 가지 질문이 생긴다:
1. 캐시가 가득 차면 뭘 내보내는가? → **LRU(Least Recently Used) 교체 정책**
2. 누군가 쓰고 있는 페이지를 내보내면 안 되지 않나? → **Pin/Unpin**
3. 수정된 페이지는 언제 디스크에 쓰는가? → **Dirty 추적과 write-back**

## LRU 캐시: O(1) 교체 정책

LRU 캐시는 HashMap + Doubly Linked List로 구현한다.

- **HashMap**: key → 연결 리스트 노드. O(1) 조회.
- **Doubly Linked List**: 가장 최근에 접근한 노드가 앞(head), 가장 오래된 노드가 뒤(tail).

접근할 때마다 해당 노드를 리스트 앞으로 옮긴다(`moveToFront`).
캐시가 가득 찬 상태에서 새 항목이 들어오면, 리스트 맨 뒤의 노드(가장 오래 안 쓴 항목)를 제거하고 새 항목을 앞에 넣는다.

Put, Get, Delete 모두 O(1)이다.

구현에서 head와 tail은 **sentinel 노드**를 쓴다. 경계 조건 처리를 단순화하기 위한 기법으로, 실제 데이터는 없고 리스트의 양 끝을 표시하는 역할만 한다.

## 페이지 관리: pin, dirty, eviction

### Page 구조
```
PageID: "path/to/file.db:3"  (파일 경로 + 페이지 번호)
Data:   []byte               (pageSize 바이트)
Dirty:  bool                 (수정됐는지)
PinCount: int                (현재 사용 중인 참조 수)
```

### FetchPage
1. 캐시에 있으면 → PinCount 증가, 같은 Page 반환 (디스크 I/O 없음)
2. 캐시에 없으면 → 파일에서 해당 offset의 pageSize 바이트를 읽어 Page 생성 → 캐시에 넣음
3. 캐시에 넣을 때 eviction이 발생하면:
   - 퇴출 대상의 PinCount > 0이면 → **에러** (pinned page는 퇴출 불가)
   - 퇴출 대상이 Dirty면 → 디스크에 write-back 후 퇴출

### UnpinPage
PinCount를 1 감소시킨다. `isDirty` 플래그로 이 페이지가 수정됐음을 표시할 수 있다.
PinCount가 0이 되면 LRU 교체 대상이 된다.

### FlushPage / FlushAll
Dirty 페이지를 디스크에 쓰고 Dirty 플래그를 false로 바꾼다.
`FlushAll`은 캐시의 모든 dirty 페이지를 flush한다.

### Close
FlushAll → 모든 파일 핸들 닫기.

## PageID 설계: "filePath:pageNumber"

PageID를 `파일 경로:페이지 번호` 형태의 문자열로 설계한 것은 의도적이다.
여러 파일에 걸친 페이지를 하나의 buffer pool로 관리할 수 있고, 파일 핸들을 pool 내부에서 lazy하게 관리한다.

`parsePageID`는 마지막 `:` 위치에서 분리한다. 파일 경로에 `:`가 있을 수 있으므로(Windows 드라이브 문자 등), `LastIndex`를 사용한다.

## 테스트로 확인한 것

4개 테스트:

- **디스크에서 fetch**: 64바이트 페이지 10개를 미리 기록한 파일에서 특정 페이지를 읽는지
- **캐시 히트**: 같은 PageID를 두 번 fetch하면 같은 Page 포인터가 반환되는지
- **dirty 추적**: 데이터를 수정하고 UnpinPage(dirty=true) → Page.Dirty가 true인지
- **eviction**: 용량이 2인 pool에서 3번째 페이지를 fetch → unpin된 LRU 페이지가 퇴출되는지

## 돌아보며

Buffer Pool은 데이터베이스 내부에서 가장 "시스템 프로그래밍에 가까운" 구성요소다.

메모리 관리, 참조 카운팅, write-back 정책 — 이런 것들이 OS의 페이지 캐시와 같은 역할을 하지만, 데이터베이스가 직접 관리함으로써 **교체 정책을 워크로드에 맞게 튜닝**할 수 있다.

다음 프로젝트(08-btree-index-and-query-scan)에서는 buffer pool 위에 B+Tree와 query scan을 올리고, 그 다음 09-mvcc에서 여러 트랜잭션의 동시성 제어를 다룬다.
