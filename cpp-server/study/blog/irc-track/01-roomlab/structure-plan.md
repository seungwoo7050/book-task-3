# roomlab structure plan

`roomlab`은 기능 설명만 하면 금방 README처럼 평평해진다. 그래서 시리즈는 "subset 서버가 어디서부터 세션을 갖고, 어떻게 room lifecycle을 만들고, 마지막에 cleanup으로 어떻게 닫히는가"가 따라가도록 설계한다. 독자가 capstone과 비교할 준비를 하는 문서라고 생각하면 자연스럽다.

## 10-registration-and-server-surface.md

첫 글은 `Connection`과 `Server`가 커지는 장면에서 시작한다. `Parser::make_messages()`와 `Executor::process()`가 event loop에 붙는 순간, runtime 위에 IRC 세션이 올라선다는 점을 보여 주는 것이 핵심이다. `Executor::process()`, `_execute_pass()`, `_execute_user()`를 통해 subset의 실제 공개 command surface도 함께 고정한다.

## 20-channel-lifecycle-and-cleanup.md

둘째 글은 channel을 기능이 아니라 데이터 구조로 읽게 만든다. `_execute_join()`, `_execute_part()`, `Channel::part()`를 중심으로, `server.chandb`와 `node->chandb`라는 두 인덱스를 같이 유지해야 하는 이유를 설명한다. 이 단계에서 capstone과 공유하는 바탕 구조도 자연스럽게 드러나야 한다.

## 30-delivery-cleanup-and-verification.md

마지막 글은 `PRIVMSG`, `NOTICE`, `QUIT`, `_disconnect()`와 smoke test를 한 줄로 잇는 데 집중한다. `make clean && make test`, `roomlab smoke passed.`를 닫는 신호로 두고, 지금 proof된 범위와 아직 dispatcher가 닫아 둔 advanced command 범위를 함께 적는다.

