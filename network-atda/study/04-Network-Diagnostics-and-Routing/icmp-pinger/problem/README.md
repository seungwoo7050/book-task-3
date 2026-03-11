# ICMP Pinger 문제 안내

## 이 문서의 역할

이 문서는 `ICMP Pinger`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 문제 목표

raw socket으로 ICMP Echo Request 패킷을 직접 만들고, Echo Reply를 받아 RTT와 손실 통계를 계산하는 `ping` 유틸리티를 구현합니다.

## 구현해야 할 동작

### ICMP 패킷 생성

- Type `8`(Echo Request), Code `0` 형식으로 패킷을 만듭니다.
- 인터넷 체크섬 알고리즘으로 checksum을 계산합니다.
- identifier, sequence number, RTT 계산용 timestamp payload를 넣습니다.

### Raw socket 사용

- `socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)` 형태의 raw socket을 엽니다.
- `sendto()`로 직접 만든 패킷을 보내고 `recvfrom()`으로 응답을 받습니다.
- 수신 데이터에서는 IP 헤더를 건너뛰고 ICMP 본문을 파싱해야 합니다.

### 응답 처리

- ICMP type이 `0`(Echo Reply)인지 확인합니다.
- identifier가 내가 보낸 요청과 같은지 확인합니다.
- 패킷 안의 timestamp로 RTT를 계산합니다.

### 통계 출력

- 전송/수신 패킷 수와 손실률을 계산합니다.
- 최소/평균/최대 RTT를 출력합니다.

## 제공 자료와 실행 환경

- starter code: `code/icmp_pinger_skeleton.py`
- 검증 스크립트: `script/test_icmp.sh`
- 실행 예시: `sudo python3 icmp_pinger_skeleton.py <target_host>`

## 제약과 해석 기준

- Python 3 표준 라이브러리만 사용합니다.
- 반드시 raw ICMP socket을 사용합니다.
- 인터넷 체크섬을 직접 구현합니다.
- live 실행에는 관리자 권한이 필요합니다.

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 패킷 생성 | ICMP Echo Request 형식이 올바릅니다. |
| 체크섬 | 인터넷 체크섬이 정확합니다. |
| 응답 파싱 | Echo Reply를 올바르게 추출하고 검증합니다. |
| RTT 측정 | RTT를 올바르게 계산합니다. |
| 통계 | 최소/평균/최대 RTT와 손실률이 정확합니다. |
| 코드 품질 | 구조가 명확하고 문서화가 된 코드입니다. |

## 출력 예시

```text
PING google.com (142.250.80.46): 64 bytes
64 bytes from 142.250.80.46: icmp_seq=1  RTT=12.345 ms
...
--- google.com ping statistics ---
4 packets sent, 4 received, 0.0% loss
RTT min/avg/max = 11.234/12.456/13.456 ms
```
