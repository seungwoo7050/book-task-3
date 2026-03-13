# roomlab 2. channel lifecycle을 양방향 인덱스로 관리하기

등록이 끝나면 roomlab의 중심은 자연스럽게 [`cpp/src/execute_join.cpp`](../../../irc-track/01-roomlab/cpp/src/execute_join.cpp)로 옮겨 간다. 여기서 흥미로운 점은 room을 만든다는 일이 `JOIN` 응답 한 줄을 보내는 것보다 훨씬 구조적인 문제라는 사실이다. 서버와 사용자 양쪽에서 membership을 동시에 기억하지 않으면 cleanup이 금세 흐트러진다.

[`cpp/include/inc/Channel.hpp`](../../../irc-track/01-roomlab/cpp/include/inc/Channel.hpp)의 `Channel`은 `clientdb`, `privdb`, `invitedb`, `state`, `limit`, `topic`, `key`를 가진다. roomlab이 core subset을 표방해도 데이터 구조는 이미 capstone까지 염두에 두고 있다. 다만 지금은 dispatcher가 advanced command를 열지 않기 때문에, 이 구조는 먼저 안전한 lifecycle을 만드는 데 쓰인다.

`_execute_join()`이 그 장면을 잘 보여 준다. channel이 없으면 새 `Channel`을 만들고 founder를 operator로 넣는다. 이미 있으면 key, limit, invite-only 조건을 확인한 뒤 기존 room에 합류시킨다. 중요한 것은 새 room이 생길 때 `server.chandb`에만 넣지 않고, 사용자의 `node->chandb`에도 동시에 넣는다는 점이다.

```cpp
Channel *chan = new Channel(*it, node);
server.chans.push_front(chan);
server.chandb.insert(...);
node->chandb.insert(...);
```

이 구조 덕분에 `_execute_part()`와 `JOIN 0`은 단순히 방에서 나가는 것이 아니라, 양쪽 인덱스를 함께 정리하는 공통 cleanup path가 된다. 먼저 `PART`를 방송하고, 그다음 사용자 쪽 map에서 room을 지우고, 마지막에 channel 쪽 `clientdb`와 `privdb`, `invitedb`를 정리한다. channel이 비면 서버의 `chans`와 `chandb`에서도 제거하고 메모리를 해제한다.

그래서 roomlab의 둘째 글에서 중요한 것은 기능이 많아 보이는가가 아니다. membership이 어디에 저장되고, 어떤 순서로 지워지는지가 더 중요하다. 뒤의 capstone이 mode와 invite를 얹더라도, room이 만들어지고 사라지는 뼈대는 이미 여기서 다 잡혀 있기 때문이다.

