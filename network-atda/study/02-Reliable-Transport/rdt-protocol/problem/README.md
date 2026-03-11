# RDT Protocol 문제 안내

## 이 문서의 역할

이 문서는 `RDT Protocol`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 문제 목표

손실과 손상이 있는 채널 위에서도 데이터를 순서대로 정확하게 전달하는 신뢰 전송 프로토콜을 구현합니다. 이 프로젝트에서는 `rdt3.0`과 `Go-Back-N` 두 가지를 모두 다룹니다.

## 구현해야 할 동작

### `rdt3.0` 송신자

- 애플리케이션에서 데이터를 받아 checksum, 시퀀스 번호, payload를 넣은 패킷을 만듭니다.
- 패킷을 보낸 뒤 timer를 시작하고 ACK를 기다립니다.
- 정상 ACK를 받으면 다음 데이터로 넘어가고, timeout이 나면 현재 패킷을 재전송합니다.
- 손상되었거나 잘못된 ACK는 무시하고 timeout을 기다립니다.

### `rdt3.0` 수신자

- 패킷을 받으면 checksum을 확인합니다.
- 기대한 시퀀스 번호이면서 손상되지 않았으면 애플리케이션에 전달하고 ACK를 보냅니다.
- 손상되었거나 중복이면 이전 ACK를 다시 보냅니다.

### `Go-Back-N` 송신자

- 윈도우 크기 `N`을 유지하며 여러 패킷을 연속해서 보냅니다.
- 누적 ACK가 도착하면 해당 번호까지 윈도우를 앞으로 밀어냅니다.
- timeout이 발생하면 현재 윈도우의 모든 미확인 패킷을 재전송합니다.

### `Go-Back-N` 수신자

- 기대하는 시퀀스 번호만 수용합니다.
- 기대한 패킷이 오면 전달 후 ACK를 보내고 기대 번호를 증가시킵니다.
- 그 외 패킷은 버리고 마지막 정상 수신 패킷의 ACK를 다시 보냅니다.

### 패킷 형식

- `Checksum(4B) + Seq Number(4B) + Payload(variable)` 형식을 유지합니다.
- checksum은 `(seq_number + payload)`의 MD5에서 앞 4바이트를 사용합니다.

## 제공 자료와 실행 환경

- 채널 시뮬레이터: `code/channel.py`
- 패킷 helper: `code/packet.py`
- starter code: `code/rdt3_skeleton.py`, `code/gbn_skeleton.py`
- 테스트 데이터: `data/test_messages.txt`
- 검증 스크립트: `script/test_rdt.sh`

## 제약과 해석 기준

- Python 3 표준 라이브러리만 사용합니다.
- 제공된 channel simulator는 수정하지 않습니다.
- checksum으로 손상을 감지해야 합니다.
- timer 값은 설정 가능해야 합니다.

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 정확한 전달 | 모든 데이터가 순서대로 손상 없이 수신됩니다. |
| 손실 처리 | loss가 발생하면 재전송으로 복구합니다. |
| 손상 처리 | checksum으로 손상된 패킷을 감지합니다. |
| 중복 처리 | 중복 패킷을 다시 애플리케이션에 전달하지 않습니다. |
| GBN 윈도우 | 송신자가 sliding window를 올바르게 유지합니다. |
| 코드 품질 | 구조가 명확하고 문서화가 된 코드입니다. |

## 출력 예시

```text
[SENDER] Sending packet seq=0: "Hello"
[CHANNEL] Packet seq=0 delivered
[RECEIVER] Received packet seq=0: "Hello" -> ACK 0
...
[SENDER] All data transferred successfully.
```
