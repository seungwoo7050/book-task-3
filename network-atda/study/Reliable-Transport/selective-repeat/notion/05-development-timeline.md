# 05 개발 타임라인

이 문서는 `Selective Repeat`를 처음 재현하는 학생을 위한 실행 순서다. 핵심은 sender의 패킷별 타이머와 receiver의 out-of-order 버퍼를 실제 코드와 테스트 기준으로 확인하는 것이다.

## 준비
- `python3`
- `pytest`
- 작업 위치: 저장소 루트 `/Users/woopinbell/work/book-task-3/network-atda`

## 단계 1. 문제와 제공물 확인
먼저 아래 파일을 읽는다.
- [`../problem/README.md`](../problem/README.md)
- [`../problem/code/channel.py`](../problem/code/channel.py)
- [`../problem/code/packet.py`](../problem/code/packet.py)
- [`../problem/code/selective_repeat_skeleton.py`](../problem/code/selective_repeat_skeleton.py)

여기서 확인할 질문:
- SR에서 새로 필요한 상태가 무엇인가
- 왜 동일 채널/패킷 모듈을 유지하는가
- 무엇이 GBN과 가장 크게 다른가

## 단계 2. 구현과 테스트 기준을 먼저 본다
- [`../python/src/selective_repeat.py`](../python/src/selective_repeat.py)
- [`../python/tests/test_selective_repeat.py`](../python/tests/test_selective_repeat.py)

이 단계에서 볼 포인트:
- `acked` 집합과 `timers` 사전이 어디서 갱신되는가
- receiver buffer가 언제 flush 되는가
- 자동 테스트가 무엇을 최소 보장으로 삼는가

## 단계 3. 자동 검증 먼저 실행
아래 명령으로 현재 상태를 먼저 고정한다.

```bash
make -C study/Reliable-Transport/selective-repeat/problem test
```

기대 결과:
- Selective Repeat 검증 스크립트가 통과한다.
- 메시지 fixture를 끝까지 전달한다.

세부 테스트는 아래로 확인한다.

```bash
cd study/Reliable-Transport/selective-repeat/python/tests
python3 -m pytest test_selective_repeat.py -v
```

## 단계 4. 수동으로 sender/receiver 상태를 다시 본다
아래 명령으로 현재 구현을 직접 실행한다.

```bash
make -C study/Reliable-Transport/selective-repeat/problem run-solution
```

기대 결과:
- 손실/손상 환경에서도 실행이 멈추지 않고 종료된다.
- timeout이 난 패킷만 선택적으로 재전송된다.
- out-of-order 수신이 있어도 상위 전달 순서는 유지된다.

## 단계 5. 실패하면 가장 먼저 볼 곳
- out-of-order 패킷이 바로 전달되면 receiver buffer와 flush 조건을 먼저 확인한다.
- 전체 윈도 재전송이 보이면 per-packet timer가 아닌 전역 timeout 로직이 남아 있지 않은지 본다.
- 중복 패킷에서 sender가 오래 기다리면 duplicate ACK 재전송 여부를 확인한다.
- 관련 근거는 [`02-debug-log.md`](02-debug-log.md)에 정리했다.

## 단계 6. 완료 판정
아래 조건을 만족하면 이 프로젝트는 재현한 것으로 본다.
- `make test`가 통과한다.
- 수동 실행이 끝까지 종료된다.
- GBN과 비교해 SR이 왜 더 복잡한 상태를 요구하는지 설명할 수 있다.
- receiver buffer와 per-packet timer의 역할을 각각 설명할 수 있다.
