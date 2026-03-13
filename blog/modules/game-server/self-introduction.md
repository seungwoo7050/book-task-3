# Game Server 자소서 Module

저는 게임서버를 단순 요청/응답 백엔드의 연장선이 아니라, authoritative state와 네트워크 조건을 함께 설계해야 하는 별도 문제라고 생각합니다. 그래서 `cpp-server`, `network-atda`, `cs-core`를 따라가며 실시간 서버 문제를 더 직접적으로 다뤄 왔습니다.

`Tactical Arena Server`에서는 TCP control protocol과 UDP packet을 함께 설계했고, `arenaserv`에서는 pure TCP 상태 머신을 구현하며 reconnect grace와 세션 연속성을 검증했습니다. 화려한 기능보다 어떤 상태를 어디서 검증할지 먼저 정하는 방식이 제 작업 습관이 됐습니다.

제가 게임서버 역할에 적합하다고 생각하는 이유는 C++를 사용했다는 사실보다, 네트워크와 상태를 함께 다루는 문제를 꾸준히 추적해 왔기 때문입니다. proxy, reliable transport, routing, shell lab 같은 기반 학습도 별도 결과물로 남겼습니다.

협업에서도 실시간 서버 문제는 특히 설명이 모호해지기 쉽다고 생각합니다. 그래서 README, 테스트 하네스, 검증 명령을 함께 남기며 상태 전이와 프로토콜 경계를 분명하게 정리하려고 합니다.

입사 후에는 현재 게임의 핵심 서버 흐름과 프로토콜 경계를 빠르게 이해하고, 신뢰할 수 있는 서버 기능을 구현하는 동시에 검증 기준을 명확히 정리하는 데 기여하고 싶습니다.
