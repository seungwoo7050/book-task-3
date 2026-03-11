# Python 구현 안내

## 이 폴더의 역할
이 디렉터리는 `Selective Repeat`의 공개 구현을 담습니다. `problem/`의 제공 자료와 분리된 사용자 작성 답안을 이 폴더에서 확인합니다.

## 먼저 볼 파일
- `python/src/selective_repeat.py` - 핵심 구현 진입점입니다.
- `python/tests/test_selective_repeat.py` - 검증 의도와 보조 테스트를 확인합니다.

## 기준 명령
- 검증: `make -C study/02-Reliable-Transport/selective-repeat/problem test`

## 현재 범위
`Go-Back-N`의 한계를 보강하기 위해 추가한 선택 재전송 프로젝트입니다.

## 남은 약점
- 실제 병렬 스레드 모델은 아닙니다.
- sequence wraparound는 구현하지 않았습니다.
- 성능 비교 표는 아직 정리하지 않았습니다.
