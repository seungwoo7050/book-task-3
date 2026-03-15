# Selective Repeat 개발 타임라인

현재 구현을 다시 읽으면 이 lab의 핵심은 "GBN을 조금 더 효율적으로 고쳤다"가 아니다. 실제 전환은 sender와 receiver가 기억해야 할 상태를 packet 단위로 늘리면서, ACK와 delivery를 분리 가능한 구조로 바꾸는 데 있다. 코드 기준 전환점은 네 번으로 정리된다.

## 1. sender는 window 하나가 아니라 packet별 상태를 들기 시작한다

출발점은 `acked` 집합과 `timers` 딕셔너리다. GBN에서는 oldest outstanding packet 기준 timer 하나면 충분했지만, Selective Repeat에서는 어떤 packet은 ACK됐고 어떤 packet은 아직 아닌 상황이 흔하다. 그래서 sender는 window 전체를 다시 보내지 않고, timeout 난 `seq`만 골라 다시 보낼 수 있다.

이번 재실행 로그도 정확히 그렇게 나왔다. `Retransmitting seq=0`, `Retransmitting seq=2`, `Retransmitting seq=4`처럼 범위가 아니라 개별 packet만 다시 전송됐다. 이 한 줄이 GBN과 가장 크게 갈라지는 지점이다.

## 2. receiver는 out-of-order를 버리지 않고 buffer에 붙잡는다

receiver 전환점은 `recv_buffer`다. `recv_base <= seq < recv_base + window_size` 범위 안이면 순서가 어긋나도 버리지 않고 저장한 뒤 즉시 ACK를 보낸다. 즉 ACK는 "받았다"를 뜻하고, delivery는 "앞 구멍까지 메워졌다"를 뜻한다.

실행 로그에서는 `Buffered seq=1 → ACK 1`, `Buffered seq=3 → ACK 3`가 먼저 찍혔고, 그 시점에는 application delivery가 일어나지 않았다. 이 구조 덕분에 sender는 이미 성공적으로 도착한 packet을 다시 보낼 필요가 줄어든다.

## 3. 앞선 결손이 메워지면 receiver는 한꺼번에 in-order delivery를 수행한다

`while recv_base in recv_buffer` 루프가 이 lab의 두 번째 핵심이다. 예를 들어 `seq=1`이 먼저 왔더라도 `seq=0`이 없으면 전달하지 않는다. 이후 `seq=0`이 오면 그제야 `0`, `1`을 연속으로 전달할 수 있다.

2026-03-14 재실행에서도 `seq=1`이 먼저 buffer된 뒤, `seq=0` 재전송이 성공하자 `Delivered seq=0`, `Delivered seq=1`이 연달아 출력됐다. 이 동작은 "out-of-order 수용"과 "in-order delivery 보장"을 동시에 성립시키는 현재 구현의 핵심이다.

## 4. duplicate와 window boundary 처리도 packet별로 더 세분된다

이 구현은 duplicate old packet과 future out-of-window packet을 다르게 다룬다. 이미 전달이 끝난 `seq < recv_base`는 re-ACK를 보내고, 너무 미래인 packet은 그냥 무시한다. sender도 ACK를 받으면 곧바로 `timers.pop(ack_seq, None)`으로 해당 packet timer만 제거한다.

즉 Selective Repeat는 단순히 재전송 횟수를 줄이는 기법이 아니라, sender와 receiver 모두 더 미세한 상태 전이를 감수하는 설계다. 이 lab를 통해 다음에 배워야 할 것은 "어느 정도 상태 복잡도까지 감당할 가치가 있는가"라는 판단 기준이다.

## 지금 남는 한계

구현은 교육용으로 충분하지만 완전한 SR 스택은 아니다. sequence wraparound가 없고, timer는 thread가 아니라 loop 순회로 처리되며, GBN 대비 성능 수치는 별도로 정리하지 않았다. 그래도 selective ACK, receiver buffering, in-order drain이라는 세 핵심 축은 현재 코드와 재실행 로그로 분명하게 확인된다.
