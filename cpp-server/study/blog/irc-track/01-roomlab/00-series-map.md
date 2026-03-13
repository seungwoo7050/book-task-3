# roomlab series map

`roomlab`은 IRC 문법을 넓게 훑는 문서가 아니다. 이 시리즈를 세 편으로 나눈 이유는, subset 서버가 실제로 커지는 지점을 registration, channel lifecycle, delivery/cleanup 세 장면으로 나눠야 capstone과의 차이가 선명해지기 때문이다.

첫 글은 runtime 위에 IRC 세션 상태가 어떻게 붙는지를 본다. 둘째 글은 room을 만드는 일보다, membership을 양방향 인덱스로 관리하고 정리하는 일이 왜 중요한지를 따라간다. 마지막 글은 `PRIVMSG`, `NOTICE`, `QUIT`, duplicate nick, cleanup이 하나의 smoke test 안에서 어떻게 맞물리는지로 닫는다.

## 글 순서

1. [10-registration-and-server-surface.md](10-registration-and-server-surface.md)
2. [20-channel-lifecycle-and-cleanup.md](20-channel-lifecycle-and-cleanup.md)
3. [30-delivery-cleanup-and-verification.md](30-delivery-cleanup-and-verification.md)

