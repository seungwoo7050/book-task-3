# UDP Pinger 문제 안내

## 이 문서의 역할

이 문서는 `UDP Pinger`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 문제 목표

UDP ping 서버에 10개의 ping 메시지를 보내고, 응답이 돌아온 경우 RTT를 계산한 뒤 최소/평균/최대 RTT와 손실률을 출력하는 클라이언트를 구현합니다.

## 구현해야 할 동작

### Ping 메시지 전송

- 정확히 10개의 UDP ping 메시지를 보냅니다.
- 각 메시지에는 시퀀스 번호와 타임스탬프를 포함합니다.
- 형식은 `Ping <sequence_number> <timestamp>`를 기준으로 합니다.

### RTT 측정

- 각 ping 전송 직전에 시간을 기록합니다.
- 응답이 오면 `응답 시각 - 전송 시각`으로 RTT를 계산합니다.

### Timeout 처리

- 각 ping에 대해 소켓 timeout을 1초로 둡니다.
- 1초 안에 응답이 없으면 `Request timed out`으로 처리합니다.

### 통계 출력

- 응답이 온 각 ping의 RTT를 출력합니다.
- 모든 전송이 끝나면 최소/평균/최대 RTT와 패킷 손실률을 출력합니다.

## 제공 자료와 실행 환경

- 제공 서버: `code/udp_pinger_server.py`
- 클라이언트 skeleton: `code/udp_pinger_client_skeleton.py`
- 검증 스크립트: `script/test_pinger.sh`

## 제약과 해석 기준

- Python 3 표준 라이브러리만 사용합니다.
- 제공된 서버 코드는 수정하지 않습니다.
- 클라이언트는 제공 서버와 프로토콜 변경 없이 동작해야 합니다.

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 정확한 메시지 전송 | 10개의 UDP ping 메시지를 형식에 맞게 전송합니다. |
| RTT 계산 | 응답이 온 ping마다 RTT를 올바르게 계산합니다. |
| Timeout 처리 | 1초 안에 응답이 없으면 손실로 판정합니다. |
| 통계 출력 | 최소/평균/최대 RTT와 손실률이 올바릅니다. |
| 코드 품질 | 간결하고 읽기 쉬운 Python 코드입니다. |

## 출력 예시

```text
Ping  1: Reply from 127.0.0.1  RTT = 0.324 ms
Ping  2: Request timed out
...
--- Ping Statistics ---
10 packets sent, 7 received, 30.0% loss
RTT min/avg/max = 0.289/0.415/0.612 ms
```
