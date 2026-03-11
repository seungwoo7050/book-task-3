# 04 지식 인덱스

## 핵심 용어
- **alternating bit**: stop-and-wait에서 송신 패킷과 ACK를 구분하기 위해 0/1 시퀀스를 번갈아 쓰는 방법이다.
- **cumulative ACK**: 해당 번호까지 연속으로 잘 받았음을 한 번에 알리는 ACK 방식이다.
- **`base`**: GBN sender 윈도에서 아직 ACK를 받지 못한 가장 앞 패킷 번호다.
- **timeout retransmission**: 정해진 시간 안에 ACK가 오지 않을 때 패킷을 다시 보내는 동작이다.

## 다시 볼 파일
- [`../problem/code/channel.py`](../problem/code/channel.py): 손실/손상 채널이 어떤 인터페이스로 노출되는지 확인할 수 있다.
- [`../problem/code/packet.py`](../problem/code/packet.py): 패킷 checksum과 ACK 형식의 기준 구현이다.
- [`../python/src/rdt3.py`](../python/src/rdt3.py): stop-and-wait 상태 기계가 가장 직접적으로 드러난다.
- [`../python/src/gbn.py`](../python/src/gbn.py): 윈도 관리와 누적 ACK 처리를 읽을 때 중심이 되는 파일이다.

## 자주 쓰는 확인 명령
- `make -C study/02-Reliable-Transport/rdt-protocol/problem test`
- `cd study/02-Reliable-Transport/rdt-protocol/python/tests && python3 -m pytest test_rdt.py -v`

## 참고 자료
- [`../docs/references/README.md`](../docs/references/README.md): 공개 문서를 정리할 때 다시 확인한 근거 모음
