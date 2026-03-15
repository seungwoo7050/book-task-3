# UDP Pinger 시리즈 맵

이 lab의 중심은 UDP가 얼마나 단순한가가 아니라, 그 단순함이 클라이언트 코드에 어떤 책임을 남기는가다. 현재 구현은 재전송이나 연결 상태를 제공하지 않는 대신, 1초 timeout, RTT 측정, loss percentage 계산을 애플리케이션 레벨에서 직접 처리한다.

## 이 lab를 읽는 질문

- 왜 UDP ping에서는 timeout이 곧 손실 판정인가
- RTT 통계는 어떤 최소 구조만으로도 유의미해질 수 있는가
- connectionless socket이라서 테스트와 출력이 어떻게 달라지는가

## 이번에 고정한 사실

- ping은 총 10번 전송한다.
- 각 ping은 `Ping <seq> <timestamp>` 형식이다.
- 응답이 오면 RTT를 ms 단위로 기록한다.
- timeout이면 즉시 `Request timed out`로 출력한다.
- 마지막에 sent/received/loss/min/avg/max를 정리한다.
