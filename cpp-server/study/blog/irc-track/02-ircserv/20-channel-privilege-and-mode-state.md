# ircserv 2. channel privilege와 mode state를 실제 모델로 바꾸기

capstone의 중심이 정말 잘 드러나는 곳은 [`cpp/src/Channel.cpp`](../../../irc-track/02-ircserv/cpp/src/Channel.cpp)와 [`cpp/src/Executor.cpp`](../../../irc-track/02-ircserv/cpp/src/Executor.cpp)다. roomlab에서도 `Channel` 구조는 이미 준비돼 있었지만, ircserv에 와서야 그 구조가 실제 권한 모델로 살아 움직인다.

`Channel`은 `clientdb` 외에 `privdb`, `invitedb`, 그리고 `lbit`, `ibit`, `tbit`, `kbit` 네 개의 mode bit를 가진다. 그래서 이제 channel은 단순한 방이 아니라, 누가 operator인지, 초대가 필요한지, topic을 누가 바꿀 수 있는지, key와 limit가 걸려 있는지를 모두 기억하는 상태 객체가 된다.

이 상태가 가장 선명하게 보이는 곳은 [`_execute_mode()`](../../../irc-track/02-ircserv/cpp/src/Executor.cpp)다. 함수는 먼저 사용자가 channel에 속해 있는지, operator 권한이 있는지 확인한 뒤, `+i`, `+t`, `+k`, `+l`, `+o`를 차례로 적용한다.

```cpp
case 'i':
    if (adding)
        channel->state |= Channel::ibit;
    else
        channel->state &= ~Channel::ibit;
    break;
```

`+k`는 key 문자열을 검증하고, `+l`은 limit를 숫자로 바꾸고, `+o`는 대상 사용자가 실제 member인지 다시 확인한 뒤 `privdb`를 갱신한다. mode 처리가 끝나면 변경 내용을 channel 전체에 broadcast하고, 현재 mode string까지 되돌려 준다. 즉 ircserv의 mode는 단순 플래그 토글이 아니라, membership 검사와 reply contract를 함께 품고 있다.

`TOPIC`과 `INVITE`는 이 state가 실제로 쓰이는 장면이다. `_execute_topic()`은 `+t`가 켜져 있으면 operator만 topic을 바꾸게 하고, `topic_setter`와 `topic_time`도 함께 저장한다. `_execute_invite()`는 `+i` 상태에서 operator만 타 사용자를 초대하게 하고, 그 사용자를 `invitedb`에 넣는다. 그리고 [`_execute_join()`](../../../irc-track/02-ircserv/cpp/src/execute_join.cpp)은 나중에 invite-only room에 들어올 때 바로 그 `invitedb`를 확인한다.

이렇게 읽으면 ircserv의 둘째 글은 "명령이 더 늘어났다"는 요약보다 훨씬 또렷하다. roomlab에서 미리 준비해 둔 자료구조가 capstone에서 비로소 실제 권한 모델과 상태 전이의 중심으로 올라오는 순간을 따라가는 글이 된다.

