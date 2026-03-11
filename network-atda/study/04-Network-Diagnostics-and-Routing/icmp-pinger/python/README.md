# Python 구현 안내

## 이 폴더의 역할
이 디렉터리는 `ICMP Pinger`의 공개 구현을 담습니다. `problem/`의 제공 자료와 분리된 사용자 작성 답안을 이 폴더에서 확인합니다.

## 먼저 볼 파일
- `python/src/icmp_pinger.py` - 핵심 구현 진입점입니다.
- `python/tests/test_icmp_pinger.py` - 검증 의도와 보조 테스트를 확인합니다.

## 기준 명령
- 검증: `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`

## 현재 범위
Raw socket으로 `ICMP Echo Request/Reply`를 직접 구현하는 진단 도구 과제입니다.

## 남은 약점
- IPv6/ICMPv6는 지원하지 않습니다.
- 시스템 `ping` 수준의 상세 통계는 제공하지 않습니다.
- live raw-socket 실행은 OS와 방화벽 정책에 영향을 받습니다.
