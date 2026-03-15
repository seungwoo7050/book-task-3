# rdt-protocol 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 정확한 전달: 모든 데이터가 순서대로 손상 없이 수신됩니다, 손실 처리: loss가 발생하면 재전송으로 복구합니다, 손상 처리: checksum으로 손상된 패킷을 감지합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `gbn_send_receive`와 `main`, `rdt_send_receive` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 정확한 전달: 모든 데이터가 순서대로 손상 없이 수신됩니다.
- 손실 처리: loss가 발생하면 재전송으로 복구합니다.
- 손상 처리: checksum으로 손상된 패킷을 감지합니다.
- 첫 진입점은 `../study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py`이고, 여기서 `gbn_send_receive`와 `main` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py`: `gbn_send_receive`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-Reliable-Transport/rdt-protocol/python/src/rdt3.py`: `rdt_send_receive`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-Reliable-Transport/rdt-protocol/problem/code/channel.py`: `UnreliableChannel`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-Reliable-Transport/rdt-protocol/problem/code/gbn_skeleton.py`: `gbn_send`, `gbn_receive`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-Reliable-Transport/rdt-protocol/problem/code/packet.py`: `compute_checksum`, `make_packet`, `parse_packet`, `is_corrupt`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-Reliable-Transport/rdt-protocol/problem/data/test_messages.txt`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/02-Reliable-Transport/rdt-protocol/problem/script/test_rdt.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.
- `../study/02-Reliable-Transport/rdt-protocol/python/tests/test_rdt.py`: `TestPacketModule`가 통과 조건과 회귀 포인트를 잠근다.

## 정답을 재구성하는 절차

1. `../study/02-Reliable-Transport/rdt-protocol/problem/code/channel.py`와 `../study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `TestPacketModule`이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/rdt-protocol/problem test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/rdt-protocol/problem test
```

- `../study/02-Reliable-Transport/rdt-protocol/problem/code/channel.py` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `TestPacketModule`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/rdt-protocol/problem test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py`
- `../study/02-Reliable-Transport/rdt-protocol/python/src/rdt3.py`
- `../study/02-Reliable-Transport/rdt-protocol/problem/code/channel.py`
- `../study/02-Reliable-Transport/rdt-protocol/problem/code/gbn_skeleton.py`
- `../study/02-Reliable-Transport/rdt-protocol/problem/code/packet.py`
- `../study/02-Reliable-Transport/rdt-protocol/problem/data/test_messages.txt`
- `../study/02-Reliable-Transport/rdt-protocol/problem/script/test_rdt.sh`
- `../study/02-Reliable-Transport/rdt-protocol/python/tests/test_rdt.py`
- `../study/02-Reliable-Transport/rdt-protocol/problem/Makefile`
