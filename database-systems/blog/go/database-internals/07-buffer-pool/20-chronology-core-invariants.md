# Core Invariants

## 1. page identity는 마지막 `:` 기준으로 file path와 page number를 자른다

`parsePageID()`는 `strings.LastIndex(pageID, ":")`로 마지막 콜론을 찾고, 앞부분은 path, 뒷부분은 page number로 해석한다.

즉 file path 안에 디렉터리 구분자가 있어도 마지막 `:`만 page boundary로 쓴다. buffer pool의 모든 fetch/write-back은 이 parsing contract 위에 선다.

## 2. cache hit는 page object를 재사용하면서 pin count만 올린다

`FetchPage()`의 첫 분기는 cached hit다.

```go
if cached := pool.cache.Get(pageID); cached != nil {
    page := cached.(*Page)
    page.PinCount++
    return page, nil
}
```

즉 같은 page를 다시 fetch하면 새로운 복사본을 만들지 않고 동일한 page object를 돌려주며 pin count를 증가시킨다. 테스트 `TestReturnCachedPage`도 page instance identity를 직접 확인한다.

## 3. dirty flag는 `UnpinPage(..., true)`에서만 명시적으로 올라간다

caller가 page를 수정했다는 신호는 `UnpinPage(pageID, isDirty)`에서 들어온다. 여기서 `isDirty=true`이면 page의 `Dirty`를 true로 바꾼다.

즉 buffer pool은 page bytes를 직접 감시하지 않는다. caller가 수정 사실을 신고해야 한다. docs의 [`pin-and-dirty.md`](/Users/woopinbell/work/book-task-3/database-systems/go/database-internals/projects/07-buffer-pool/docs/concepts/pin-and-dirty.md)가 바로 이 점을 설명한다.

## 4. eviction은 LRU 후보를 받되, pinned면 되돌리고 실패한다

`FetchPage()` miss path는 새 page를 `cache.Put()`으로 넣고, evicted value가 있으면 그 page를 검사한다.

- `PinCount > 0`이면 eviction 불가
- `Dirty`면 write-back 후 eviction

흥미로운 점은 pinned page가 나오면 아래처럼 eviction된 page를 cache에 다시 넣고 에러를 반환한다는 것이다.

```go
if evictedPage.PinCount > 0 {
    pool.cache.Put(evicted.Key, evictedPage)
    return nil, errors.New("bufferpool: cannot evict pinned page")
}
```

즉 현재 구현은 "다른 후보를 다시 찾는 replacer"가 아니라, pinned candidate를 만나면 바로 실패하는 단순 정책을 택한다.

## 5. dirty write-back은 explicit flush와 eviction에서만 일어난다

`FlushPage()`는 dirty가 아니면 아무것도 하지 않고, dirty면 `writePage()` 후 `Dirty=false`로 되돌린다. eviction path도 dirty page면 먼저 `writePage()`를 호출한다.

추가 재실행의 `disk_after_flush modified`는 이 계약을 직접 보여 준다. 메모리에서 `"modified"`로 바꾼 bytes가 flush 후 실제 file에 기록된다.

즉 현재 구현에서 dirty persistence는 background가 아니라 explicit call 또는 eviction 시점에만 발생한다.
