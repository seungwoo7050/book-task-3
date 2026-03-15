# selective-repeat 답안지

이 문서는 문제지를 다시 넘기지 않고도 해답을 재구성할 수 있도록, 실제 구현 파일과 테스트만 기준으로 정리한 답안지다.

## 한 줄 해답

시작 위치의 구현을 완성해 선택 재전송: timeout이 난 패킷만 다시 전송합니다, 수신 버퍼링: out-of-order 패킷을 버퍼링하고 순서대로 전달합니다, ACK 처리: 개별 ACK로 sender 상태를 정확히 갱신합니다를 한 흐름으로 설명하고 검증한다. 핵심은 `selective_repeat_send_receive`와 `load_messages`, `main` 흐름을 구현하고 테스트를 통과시키는 것이다.

## 문제를 푸는 핵심 전략

- 선택 재전송: timeout이 난 패킷만 다시 전송합니다.
- 수신 버퍼링: out-of-order 패킷을 버퍼링하고 순서대로 전달합니다.
- ACK 처리: 개별 ACK로 sender 상태를 정확히 갱신합니다.
- 첫 진입점은 `../study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`이고, 여기서 `selective_repeat_send_receive`와 `load_messages` 흐름을 먼저 붙잡은 뒤 나머지 파일로 확장한다.

## 코드 워크스루

- `../study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`: `selective_repeat_send_receive`, `load_messages`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-Reliable-Transport/selective-repeat/problem/code/channel.py`: `UnreliableChannel`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-Reliable-Transport/selective-repeat/problem/code/packet.py`: `compute_checksum`, `make_packet`, `parse_packet`, `is_corrupt`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-Reliable-Transport/selective-repeat/problem/code/selective_repeat_skeleton.py`: `selective_repeat_send`, `selective_repeat_receive`, `main`가 핵심 흐름과 상태 전이를 묶는다.
- `../study/02-Reliable-Transport/selective-repeat/problem/data/test_messages.txt`: 입력 fixture나 계약 데이터를 고정하는 근거 파일이다.
- `../study/02-Reliable-Transport/selective-repeat/problem/script/test_selective_repeat.sh`: 검증 절차나 보조 자동화를 담아 결과를 재현하는 스크립트다.
- `../study/02-Reliable-Transport/selective-repeat/python/tests/test_selective_repeat.py`: `test_selective_repeat_delivers_all_messages_without_loss`, `test_message_fixture_is_available`가 통과 조건과 회귀 포인트를 잠근다.
- `../study/02-Reliable-Transport/selective-repeat/problem/Makefile`: 실행 명령과 검증 경로를 고정하는 설정 파일이다.

## 정답을 재구성하는 절차

1. `../study/02-Reliable-Transport/selective-repeat/problem/code/channel.py`와 `../study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`를 나란히 열어 먼저 바뀌는 경계를 잡는다.
2. `test_selective_repeat_delivers_all_messages_without_loss` 등이 요구하는 순서대로 핵심 상태 전이와 예외 흐름을 채운다.
3. `make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/selective-repeat/problem test`를 실행해 결과를 잠그고, 필요하면 남은 검증 명령까지 이어서 돌린다.

## 검증과 실패 포인트

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/selective-repeat/problem test
```

- `../study/02-Reliable-Transport/selective-repeat/problem/code/channel.py` starter skeleton의 빈칸을 그대로 정답으로 착각하지 않는다.
- `test_selective_repeat_delivers_all_messages_without_loss`와 `test_message_fixture_is_available`가 잠근 상태 전이와 입력 계약을 빼먹지 않는다.
- 완성 직전에만 한 번 돌리지 말고, 상태 전이를 건드릴 때마다 `make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/selective-repeat/problem test`로 회귀를 조기에 잡는다.

## 소스 근거

- `../study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`
- `../study/02-Reliable-Transport/selective-repeat/problem/code/channel.py`
- `../study/02-Reliable-Transport/selective-repeat/problem/code/packet.py`
- `../study/02-Reliable-Transport/selective-repeat/problem/code/selective_repeat_skeleton.py`
- `../study/02-Reliable-Transport/selective-repeat/problem/data/test_messages.txt`
- `../study/02-Reliable-Transport/selective-repeat/problem/script/test_selective_repeat.sh`
- `../study/02-Reliable-Transport/selective-repeat/python/tests/test_selective_repeat.py`
- `../study/02-Reliable-Transport/selective-repeat/problem/Makefile`
