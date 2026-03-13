# Game Server 자소서

저는 게임서버를 단순히 요청과 응답을 처리하는 일반적인 백엔드의 연장선으로 보기보다, authoritative state와 네트워크 조건을 함께 설계해야 하는 별도 문제라고 생각합니다. 42서울 정규과정을 통해 시스템 프로그래밍과 네트워크의 기초를 다졌고, 이후 현재 워크스페이스에서 `cpp-server`, `network-atda`, `cs-core` 프로젝트들을 학습 순서에 맞게 구현하면서 실시간 서버 문제를 더 직접적으로 다뤄 왔습니다. 특히 입력 처리, reconnect, state transition, deterministic test 같은 지점에 큰 흥미를 느끼고 있습니다.

저는 문제를 해결할 때 화려한 기능보다 상태 전이와 검증 경계를 먼저 정하는 편입니다. `arenaserv`에서는 room queue, countdown, in-round, reconnect grace를 하나의 상태 머신으로 묶었고, `Tactical Arena Server`에서는 line-based TCP control protocol과 binary UDP packet을 함께 설계하면서 authoritative simulation을 설명 가능한 구조로 만들었습니다. 이 과정에서 bot demo, smoke test, integration harness를 함께 두어 서버의 동작을 다시 검증할 수 있게 정리했습니다.

제가 게임서버 역할에 적합하다고 생각하는 이유는 C++를 사용했다는 사실 자체보다, 네트워크와 상태를 함께 다루는 문제를 지속적으로 추적해 왔기 때문입니다. proxy, reliable transport, routing, shell lab 같은 기반 프로젝트를 통해 socket I/O, concurrency hazard, race discipline, protocol reasoning을 따로 학습했고, 그 위에서 capstone 서버를 구현했습니다. 그래서 서버 기능을 단순 CRUD처럼 보지 않고, 세션 연속성과 authoritative state를 중심으로 바라보는 편입니다.

협업에서도 저는 구현 결과를 다른 사람이 다시 따라갈 수 있게 정리하는 태도가 중요하다고 생각합니다. 실시간 서버 문제는 특히 설명이 모호해지기 쉬워서, README, 테스트 하네스, 검증 명령을 함께 남기는 습관이 더 중요하다고 느껴 왔습니다. 팀 안에서도 단순히 기능을 구현하는 사람보다, 상태 전이와 검증 기준을 명확히 정리해 주는 사람으로 기여하고 싶습니다.

입사 후에는 먼저 현재 서비스의 서버 구조와 핵심 게임 플레이 흐름을 빠르게 이해하고, 맡은 기능의 프로토콜과 상태 경계를 정확히 파악하는 데 집중하겠습니다. 그 위에서 제가 쌓아 온 C++, 네트워크, deterministic 검증 습관을 바탕으로, 단기적으로는 신뢰할 수 있는 서버 기능을 구현하는 엔지니어가 되고 싶고, 장기적으로는 authoritative server 구조와 실시간 운영 문제를 함께 설계할 수 있는 게임서버 개발자로 성장하고 싶습니다.
