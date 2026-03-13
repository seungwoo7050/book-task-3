# ircserv series map

`ircserv`은 roomlab의 subset 서버를 그대로 따라가다 마지막에 기능만 붙이는 시리즈가 아니다. 여기서 보여 주고 싶은 것은, roomlab에서 이미 준비해 둔 구조가 capstone에서 실제 command surface와 privilege/state machine으로 활성화되는 과정이다. 그래서 시리즈도 dispatcher 확장, channel privilege, end-to-end verification 순서로 나눴다.

첫 글은 baseline registration 위에 `CAP LS 302`와 advanced command routing이 열리는 장면을 다룬다. 둘째 글은 `Channel` bitset과 `TOPIC`, `INVITE`, `MODE`가 실제로 어떻게 권한 모델을 만드는지 따라간다. 마지막 글은 `KICK`, invite-only 재입장 거절, smoke verification을 통해 capstone 범위를 확실히 닫는다.

## 글 순서

1. [10-baseline-capability-and-registration.md](10-baseline-capability-and-registration.md)
2. [20-channel-privilege-and-mode-state.md](20-channel-privilege-and-mode-state.md)
3. [30-advanced-command-flows-and-verification.md](30-advanced-command-flows-and-verification.md)

