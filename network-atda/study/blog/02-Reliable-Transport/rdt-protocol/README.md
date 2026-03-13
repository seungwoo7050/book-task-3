# RDT Protocol blog

이 디렉터리는 `RDT Protocol`을 `source-first` 방식으로 다시 읽는 blog 시리즈다. chronology는 프로젝트 README, `problem/README.md`, `problem/Makefile`, `python/src/rdt3.py`, `python/src/gbn.py`, `python/tests/test_rdt.py`를 기준으로 복원했다.

## source set
- [`../../../02-Reliable-Transport/rdt-protocol/README.md`](../../../02-Reliable-Transport/rdt-protocol/README.md)
- [`../../../02-Reliable-Transport/rdt-protocol/problem/README.md`](../../../02-Reliable-Transport/rdt-protocol/problem/README.md)
- [`../../../02-Reliable-Transport/rdt-protocol/problem/Makefile`](../../../02-Reliable-Transport/rdt-protocol/problem/Makefile)
- [`../../../02-Reliable-Transport/rdt-protocol/python/src/rdt3.py`](../../../02-Reliable-Transport/rdt-protocol/python/src/rdt3.py)
- [`../../../02-Reliable-Transport/rdt-protocol/python/src/gbn.py`](../../../02-Reliable-Transport/rdt-protocol/python/src/gbn.py)
- [`../../../02-Reliable-Transport/rdt-protocol/python/tests/test_rdt.py`](../../../02-Reliable-Transport/rdt-protocol/python/tests/test_rdt.py)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../02-Reliable-Transport/rdt-protocol/README.md`](../../../02-Reliable-Transport/rdt-protocol/README.md)

## 검증 진입점
- `make -C study/02-Reliable-Transport/rdt-protocol/problem test`

## chronology 메모
- 이 프로젝트는 `rdt3.0`과 `GBN` 두 답안을 함께 읽어야 흐름이 살아난다.
- 핵심은 checksum helper보다 timeout과 ACK가 sender state를 어떻게 움직이는가에 있다.
