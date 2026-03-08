# Python 구현 안내

이 디렉터리는 `UDP Pinger`의 공개 구현을 담는다.

## 구성

- `src/udp_pinger_client.py`
- `tests/test_udp_pinger.py`

## 기준 명령

- 실행: `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem test`

## 구현 메모

- 상태: `verified`
- 현재 범위: 클라이언트 구현이 중심이다. 서버는 제공된 드롭 시뮬레이터를 그대로 사용한다.
- 남은 약점: 패킷 순서 역전은 별도 처리하지 않음
- 남은 약점: 분위수 통계 미지원
- 남은 약점: pytest는 서버 선기동 필요
