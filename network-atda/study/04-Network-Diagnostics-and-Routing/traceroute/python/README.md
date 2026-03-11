# Python 구현 안내

## 이 폴더의 역할
이 디렉터리는 `Traceroute`의 공개 구현을 담습니다. `problem/`의 제공 자료와 분리된 사용자 작성 답안을 이 폴더에서 확인합니다.

## 먼저 볼 파일
- `python/src/traceroute.py` - 핵심 구현 진입점입니다.
- `python/tests/test_traceroute.py` - 검증 의도와 보조 테스트를 확인합니다.

## 기준 명령
- 검증: `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`

## 현재 범위
TTL 증가와 `ICMP Time Exceeded`를 이용해 hop-by-hop 경로를 드러내는 bridge 프로젝트입니다.

## 남은 약점
- IPv6 traceroute는 지원하지 않습니다.
- DNS reverse lookup은 포함하지 않습니다.
- ECMP나 비대칭 경로 같은 실제 인터넷 변동성은 모델링하지 않습니다.
