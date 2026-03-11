# Python 구현 안내

## 이 폴더의 역할
이 디렉터리는 `Distance-Vector Routing`의 공개 구현을 담습니다. `problem/`의 제공 자료와 분리된 사용자 작성 답안을 이 폴더에서 확인합니다.

## 먼저 볼 파일
- `python/src/dv_routing.py` - 핵심 구현 진입점입니다.
- `python/tests/test_dv_routing.py` - 검증 의도와 보조 테스트를 확인합니다.

## 기준 명령
- 검증: `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test`

## 현재 범위
Bellman-Ford 식을 분산 라우팅 테이블 갱신으로 옮기는 시뮬레이션 과제입니다.

## 남은 약점
- poisoned reverse는 구현하지 않았습니다.
- 동적 토폴로지 변화 실험은 포함하지 않습니다.
- 비동기 메시지 모델은 구현하지 않습니다.
