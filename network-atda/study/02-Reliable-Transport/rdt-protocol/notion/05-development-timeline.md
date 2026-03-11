# 05 개발 타임라인

이 문서는 `RDT Protocol`을 처음 재현하는 학생을 위한 실행 순서다. 핵심은 `rdt3`와 `GBN`을 같은 손실 채널 위에서 비교하면서, 신뢰 전송이 어떤 상태 변수 위에 서 있는지 직접 확인하는 것이다.

## 준비
- `python3`
- `pytest`
- 작업 위치: 저장소 루트 `/Users/woopinbell/work/book-task-3/network-atda`

## 단계 1. 문제와 제공물 확인
먼저 아래 파일을 읽는다.
- [`../problem/README.md`](../problem/README.md)
- [`../problem/code/channel.py`](../problem/code/channel.py)
- [`../problem/code/packet.py`](../problem/code/packet.py)
- [`../problem/code/rdt3_skeleton.py`](../problem/code/rdt3_skeleton.py)
- [`../problem/code/gbn_skeleton.py`](../problem/code/gbn_skeleton.py)

여기서 확인할 질문:
- 어떤 부분은 제공되고 어떤 부분을 직접 구현해야 하는가
- 손실과 손상은 어떤 채널 모델로 주입되는가
- `rdt3`와 `GBN`의 차이를 어떤 기준으로 관찰할 것인가

## 단계 2. 현재 구현과 테스트 기준을 먼저 본다
- [`../python/src/rdt3.py`](../python/src/rdt3.py)
- [`../python/src/gbn.py`](../python/src/gbn.py)
- [`../python/tests/test_rdt.py`](../python/tests/test_rdt.py)

이 단계에서 볼 포인트:
- `rdt3`는 alternating bit와 단일 타이머를 어떻게 쓰는가
- GBN sender는 `base`와 `next_seq`를 어디서 관리하는가
- checksum/ACK 관련 최소 단위 테스트는 어디까지 준비되어 있는가

## 단계 3. 자동 검증 먼저 실행
가장 먼저 아래 명령으로 현재 상태를 고정한다.

```bash
make -C study/02-Reliable-Transport/rdt-protocol/problem test
```

기대 결과:
- 패킷 모듈과 전송 스크립트 검증이 통과한다.
- 손실/손상 조건에서도 메시지 전달이 끝까지 완료된다.

세부 테스트는 아래로 확인한다.

```bash
cd study/02-Reliable-Transport/rdt-protocol/python/tests
python3 -m pytest test_rdt.py -v
```

## 단계 4. `rdt3`와 `GBN`을 각각 실행해 본다
아래 두 명령을 차례대로 실행한다.

```bash
make -C study/02-Reliable-Transport/rdt-protocol/problem run-solution-rdt3
make -C study/02-Reliable-Transport/rdt-protocol/problem run-solution-gbn
```

기대 결과:
- 두 실행 모두 멈추지 않고 종료된다.
- 손실/손상 환경에서도 최종 메시지 전달이 보장된다.
- `GBN` 쪽이 timeout 시 더 넓은 재전송을 보일 수 있다.

## 단계 5. 실패하면 가장 먼저 볼 곳
- ACK 하나를 패킷 하나의 확인으로 오해하면 GBN 윈도 전진이 깨진다.
- `base`가 바뀌는데 타이머가 갱신되지 않으면 sender가 멈출 수 있다.
- duplicate packet을 receiver가 다시 전달하면 상위 메시지 순서가 깨진다.
- 관련 근거는 [`02-debug-log.md`](02-debug-log.md)에 정리했다.

## 단계 6. 완료 판정
아래 조건을 만족하면 이 프로젝트는 재현한 것으로 본다.
- `make test`가 통과한다.
- `rdt3`와 `GBN`을 각각 직접 실행했다.
- `packet.py`와 프로토콜 상태 기계의 책임 경계를 설명할 수 있다.
- `GBN`이 왜 간단하지만 불필요한 재전송을 할 수 있는지 설명할 수 있다.
