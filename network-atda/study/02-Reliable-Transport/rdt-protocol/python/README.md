# Python 구현 안내

## 이 폴더의 역할
이 디렉터리는 `RDT Protocol`의 공개 구현을 담습니다. `problem/`의 제공 자료와 분리된 사용자 작성 답안을 이 폴더에서 확인합니다.

## 먼저 볼 파일
- `python/src/gbn.py` - 핵심 구현 진입점입니다.
- `python/src/rdt3.py` - 핵심 구현 진입점입니다.
- `python/tests/test_rdt.py` - 검증 의도와 보조 테스트를 확인합니다.

## 기준 명령
- 검증: `make -C study/02-Reliable-Transport/rdt-protocol/problem test`

## 현재 범위
`rdt3.0`과 `Go-Back-N`을 같은 채널 모델 위에서 비교하는 신뢰 전송 과제입니다.

## 남은 약점
- 실제 네트워크가 아니라 시뮬레이션 채널을 사용합니다.
- GBN 성능 로그를 자동 수집하지 않습니다.
- 동시성 대신 단일 이벤트 루프를 사용합니다.
