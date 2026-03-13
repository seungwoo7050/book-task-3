# 02. Reliable Transport blog

이 트랙의 blog 시리즈는 손실과 손상 채널 위에서 sender/receiver 상태가 어떻게 바뀌는지 소스코드 기준으로 다시 정리한다. `packet.py`, `channel.py`, solution 코드, 테스트 코드를 같이 읽으며 `Stop-and-Wait -> GBN -> SR` 비교를 중심에 둔다.

## 프로젝트

| 프로젝트 | blog | 원 프로젝트 |
| :--- | :--- | :--- |
| RDT Protocol | [`README.md`](rdt-protocol/README.md) | [`../../02-Reliable-Transport/rdt-protocol/README.md`](../../02-Reliable-Transport/rdt-protocol/README.md) |
| Selective Repeat | [`README.md`](selective-repeat/README.md) | [`../../02-Reliable-Transport/selective-repeat/README.md`](../../02-Reliable-Transport/selective-repeat/README.md) |

## 읽는 순서
1. [`RDT Protocol`](rdt-protocol/README.md)에서 alternating bit와 cumulative ACK를 기준선으로 잡는다.
2. [`Selective Repeat`](selective-repeat/README.md)에서 per-packet timer와 receiver buffer가 왜 필요한지 비교한다.

## source-first 메모
- 구현형이므로 inline 증거는 `rdt3.py`, `gbn.py`, `selective_repeat.py`의 timeout/ACK/window 조각에서 뽑는다.
- CLI는 `run-solution-*`, `test`, 필요 시 fixture 기반 pytest 흐름까지 포함한다.
- git history가 세밀하지 않아 chronology는 `Day/Session`으로 재구성했다.
- 비교 흐름은 소스와 테스트가 말해 주는 범위 안에서만 추론한다.
