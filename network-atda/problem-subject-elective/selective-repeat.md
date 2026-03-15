# selective-repeat 문제지

## 왜 중요한가

이 문서는 Selective Repeat를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 목표

시작 위치의 구현을 완성해 선택 재전송: timeout이 난 패킷만 다시 전송합니다, 수신 버퍼링: out-of-order 패킷을 버퍼링하고 순서대로 전달합니다, ACK 처리: 개별 ACK로 sender 상태를 정확히 갱신합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/02-Reliable-Transport/selective-repeat/problem/code/channel.py`
- `../study/02-Reliable-Transport/selective-repeat/problem/code/packet.py`
- `../study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`
- `../study/02-Reliable-Transport/selective-repeat/problem/code/selective_repeat_skeleton.py`
- `../study/02-Reliable-Transport/selective-repeat/problem/data/test_messages.txt`
- `../study/02-Reliable-Transport/selective-repeat/problem/script/test_selective_repeat.sh`
- `../study/02-Reliable-Transport/selective-repeat/problem/Makefile`

## starter code / 입력 계약

- ../study/02-Reliable-Transport/selective-repeat/problem/code/channel.py에서 starter 코드와 입력 경계를 잡는다.
- ../study/02-Reliable-Transport/selective-repeat/problem/code/packet.py에서 starter 코드와 입력 경계를 잡는다.
- ../study/02-Reliable-Transport/selective-repeat/problem/code/selective_repeat_skeleton.py에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 선택 재전송: timeout이 난 패킷만 다시 전송합니다.
- 수신 버퍼링: out-of-order 패킷을 버퍼링하고 순서대로 전달합니다.
- ACK 처리: 개별 ACK로 sender 상태를 정확히 갱신합니다.
- 공유 helper 재사용: 기존 packet/channel 계약을 깨지 않습니다.
- 코드 품질: GBN과 비교해 읽기 쉬운 구조로 정리합니다.

## 제외 범위

- `../study/02-Reliable-Transport/selective-repeat/problem/code/channel.py` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/02-Reliable-Transport/selective-repeat/problem/data/test_messages.txt` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/02-Reliable-Transport/selective-repeat/problem/code/channel.py`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `selective_repeat_send_receive`와 `load_messages`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `test_selective_repeat_delivers_all_messages_without_loss`와 `test_message_fixture_is_available`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/02-Reliable-Transport/selective-repeat/problem/data/test_messages.txt` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/selective-repeat/problem test
```

- `selective-repeat`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`selective-repeat_answer.md`](selective-repeat_answer.md)에서 확인한다.
