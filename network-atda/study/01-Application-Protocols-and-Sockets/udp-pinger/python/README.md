# Python 구현 안내

## 이 폴더의 역할
이 디렉터리는 `UDP Pinger`의 공개 구현을 담습니다. `problem/`의 제공 자료와 분리된 사용자 작성 답안을 이 폴더에서 확인합니다.

## 먼저 볼 파일
- `python/src/udp_pinger_client.py` - 핵심 구현 진입점입니다.
- `python/tests/test_udp_pinger.py` - 검증 의도와 보조 테스트를 확인합니다.

## 기준 명령
- 검증: `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`

## 현재 범위
UDP의 비연결성과 timeout 기반 손실 처리를 RTT 측정 과제로 묶은 구현입니다.

## 남은 약점
- 패킷 순서 역전은 별도 처리하지 않습니다.
- 분위수 같은 고급 통계는 계산하지 않습니다.
- `pytest` 단독 실행은 제공 서버 선기동이 필요합니다.
