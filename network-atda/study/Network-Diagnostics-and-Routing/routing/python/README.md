# Python 구현 안내

이 디렉터리는 `Distance-Vector Routing`의 공개 구현을 담는다.

## 구성

- `src/dv_routing.py`
- `tests/test_dv_routing.py`

## 기준 명령

- 실행: `make -C study/Network-Diagnostics-and-Routing/routing/problem run-solution`
- 검증: `make -C study/Network-Diagnostics-and-Routing/routing/problem test`

## 구현 메모

- 상태: `verified`
- 현재 범위: 기본 DV 알고리즘에 집중한다. poisoned reverse와 동적 링크 변동은 문서 수준 보강에 머문다.
- 남은 약점: poisoned reverse 미구현
- 남은 약점: 동적 토폴로지 실험 부재
- 남은 약점: 비동기 메시지 모델 미구현
