# rdt-protocol 문제지

## 왜 중요한가

이 문서는 RDT Protocol를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 목표

시작 위치의 구현을 완성해 정확한 전달: 모든 데이터가 순서대로 손상 없이 수신됩니다, 손실 처리: loss가 발생하면 재전송으로 복구합니다, 손상 처리: checksum으로 손상된 패킷을 감지합니다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/02-Reliable-Transport/rdt-protocol/problem/code/channel.py`
- `../study/02-Reliable-Transport/rdt-protocol/problem/code/gbn_skeleton.py`
- `../study/02-Reliable-Transport/rdt-protocol/python/src/gbn.py`
- `../study/02-Reliable-Transport/rdt-protocol/python/src/rdt3.py`
- `../study/02-Reliable-Transport/rdt-protocol/problem/data/test_messages.txt`
- `../study/02-Reliable-Transport/rdt-protocol/problem/script/test_rdt.sh`
- `../study/02-Reliable-Transport/rdt-protocol/problem/Makefile`

## starter code / 입력 계약

- ../study/02-Reliable-Transport/rdt-protocol/problem/code/channel.py에서 starter 코드와 입력 경계를 잡는다.
- ../study/02-Reliable-Transport/rdt-protocol/problem/code/gbn_skeleton.py에서 starter 코드와 입력 경계를 잡는다.
- ../study/02-Reliable-Transport/rdt-protocol/problem/code/packet.py에서 starter 코드와 입력 경계를 잡는다.

## 핵심 요구사항

- 정확한 전달: 모든 데이터가 순서대로 손상 없이 수신됩니다.
- 손실 처리: loss가 발생하면 재전송으로 복구합니다.
- 손상 처리: checksum으로 손상된 패킷을 감지합니다.
- 중복 처리: 중복 패킷을 다시 애플리케이션에 전달하지 않습니다.
- GBN 윈도우: 송신자가 sliding window를 올바르게 유지합니다.
- 코드 품질: 구조가 명확하고 문서화가 된 코드입니다.

## 제외 범위

- `../study/02-Reliable-Transport/rdt-protocol/problem/code/channel.py` starter skeleton을 정답 구현으로 착각하지 않는다.
- `../study/02-Reliable-Transport/rdt-protocol/problem/data/test_messages.txt` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.

## 성공 체크리스트

- `../study/02-Reliable-Transport/rdt-protocol/problem/code/channel.py`의 빈 확장 지점을 실제 구현으로 채웠다.
- 핵심 흐름은 `gbn_send_receive`와 `main`가 각각 어떤 상태 전이와 계산을 맡는지 코드로 설명할 수 있다.
- 검증 기준은 `TestPacketModule`가 잠근 입력 계약과 회귀 경계를 그대로 재현하는 것이다.
- `../study/02-Reliable-Transport/rdt-protocol/problem/data/test_messages.txt` 등 fixture/trace 기준으로 결과를 대조했다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/rdt-protocol/problem test
```

- `rdt-protocol`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`rdt-protocol_answer.md`](rdt-protocol_answer.md)에서 확인한다.
