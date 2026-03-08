# Python 구현 안내

이 디렉터리는 `Traceroute`의 공개 구현을 담는다.

## 구성

- `src/traceroute.py`
- `tests/test_traceroute.py`

## 기준 명령

- 실행: `make -C study/Network-Diagnostics-and-Routing/traceroute/problem run-client HOST=8.8.8.8`
- 검증: `make -C study/Network-Diagnostics-and-Routing/traceroute/problem test`

## 구현 메모

- 상태: `verified`
- 현재 범위: 비권한 테스트가 parser/formatter와 synthetic hop discovery까지 검증한다. live hop trace는 수동 재현 명령으로 남긴다.
- 남은 약점: IPv6 traceroute 미지원
- 남은 약점: DNS reverse lookup 미포함
- 남은 약점: ECMP/비대칭 경로 같은 실제 인터넷 변동성은 모델링하지 않음
