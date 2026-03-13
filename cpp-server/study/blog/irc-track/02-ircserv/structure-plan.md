# ircserv structure plan

`ircserv`은 roomlab보다 기능이 많다는 식으로만 설명하면 금방 평면적으로 읽힌다. 이 시리즈는 대신 "무엇이 실제 capstone 차이인가"를 따라가게 설계한다. 그래서 글의 중심은 baseline registration, privilege-bearing channel state, 그리고 advanced command verification이다.

## 10-baseline-capability-and-registration.md

첫 글은 roomlab와 같은 뼈대 위에 dispatcher가 넓어지는 장면에서 시작한다. `Executor::process()`, `_execute_cap()`, `_execute_user()`를 통해 `CAP LS 302`와 registration bundle이 capstone의 baseline surface라는 점을 보여 주는 것이 핵심이다. smoke test에서 alice가 registration 전에 capability를 probing하는 장면도 여기서 함께 다룬다.

## 20-channel-privilege-and-mode-state.md

둘째 글은 `Channel.cpp`와 `_execute_mode()`, `_execute_topic()`, `_execute_invite()`, `_execute_join()`를 중심에 둔다. 독자가 "capstone의 무게중심이 command 개수보다 state model에 있다"는 점을 읽게 만드는 것이 목적이다. `i`, `t`, `k`, `l`, `o` 모드와 `privdb`, `invitedb`의 연결을 자연스럽게 풀어야 한다.

## 30-advanced-command-flows-and-verification.md

마지막 글은 `KICK`과 smoke test를 묶는다. `make clean && make test`, `ircserv capstone smoke passed.`를 닫는 신호로 두고, advanced command가 실제 cleanup과 invite-only 재입장 거절까지 버티는지 확인한다. 동시에 TLS, SASL, services 같은 의도적 비범위도 짧게 남긴다.

