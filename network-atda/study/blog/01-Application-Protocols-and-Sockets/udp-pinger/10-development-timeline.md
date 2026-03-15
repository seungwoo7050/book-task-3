# UDP Pinger 개발 타임라인

이 lab의 흐름은 구현 기능이 아니라, 신뢰성 없는 전송을 어떻게 사람이 읽을 수 있는 출력으로 바꾸는지 따라가야 한다.

## 1. 먼저 1초 timeout을 계약으로 둔다

현재 구현은 UDP socket에 `settimeout(1)`을 건다. 이 한 줄이 없으면 손실은 무한 대기와 구분되지 않는다. 즉 이 lab의 첫 설계는 네트워크가 아니라 기다림의 상한을 정하는 일이다.

## 2. 각 ping은 sequence와 timestamp를 함께 보낸다

메시지는 `Ping <seq> <timestamp>` 형식이다. sequence는 사람이 출력 순서를 읽게 하고, timestamp는 RTT 계산 근거가 된다. UDP가 연결 상태를 안 주기 때문에, 클라이언트가 직접 최소한의 문맥을 실어 보내는 셈이다.

## 3. 응답이 오면 RTT, 안 오면 손실로 기록한다

응답 성공과 timeout은 완전히 다른 출력으로 갈라진다.

- 성공: `Reply from ... RTT = ... ms`
- 실패: `Request timed out`

그래서 이 lab는 "응답을 받았다"보다 "어떤 시도가 손실로 끝났는지 보인다"가 더 중요하다.

## 4. 마지막 통계가 이 lab의 요점을 요약한다

2026-03-14 정식 재실행에서 실제로 `10 packets sent, 8 received, 20.0% loss`가 출력됐다. 그리고 `RTT min/avg/max = 0.053/0.156/0.472 ms`가 이어졌다. 즉 현재 구현은 네트워크 진단 도구의 가장 작은 단위를 이미 갖췄다. 개별 시도 로그와 전체 통계를 같이 보여 주기 때문이다.

## 지금 남는 한계

현재 범위는 의도적으로 좁다. 순서 역전, 재전송, 지터 percentile은 없다. 그 대신 connectionless transport에서 timeout과 loss를 어떻게 해석할지 집중한다.
