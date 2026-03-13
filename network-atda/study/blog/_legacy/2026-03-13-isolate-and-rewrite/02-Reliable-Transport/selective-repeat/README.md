# Selective Repeat blog

이 디렉터리는 `Selective Repeat`를 `source-first` 방식으로 다시 읽는 blog 시리즈다. chronology는 프로젝트 README, `problem/README.md`, `problem/Makefile`, `python/src/selective_repeat.py`, `python/tests/test_selective_repeat.py`를 기준으로 복원했다.

## source set
- [`../../../02-Reliable-Transport/selective-repeat/README.md`](../../../02-Reliable-Transport/selective-repeat/README.md)
- [`../../../02-Reliable-Transport/selective-repeat/problem/README.md`](../../../02-Reliable-Transport/selective-repeat/problem/README.md)
- [`../../../02-Reliable-Transport/selective-repeat/problem/Makefile`](../../../02-Reliable-Transport/selective-repeat/problem/Makefile)
- [`../../../02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`](../../../02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py)
- [`../../../02-Reliable-Transport/selective-repeat/python/tests/test_selective_repeat.py`](../../../02-Reliable-Transport/selective-repeat/python/tests/test_selective_repeat.py)

## 읽는 순서
1. [`00-series-map.md`](00-series-map.md)
2. [`10-development-timeline.md`](10-development-timeline.md)
3. [`../../../02-Reliable-Transport/selective-repeat/README.md`](../../../02-Reliable-Transport/selective-repeat/README.md)

## 검증 진입점
- `make -C study/02-Reliable-Transport/selective-repeat/problem test`

## chronology 메모
- 이 프로젝트는 `GBN`과의 차이를 설명하지 못하면 절반만 읽은 셈이다.
- 핵심 근거는 receiver buffer, per-packet timer, `send_base` 갱신 규칙이다.
