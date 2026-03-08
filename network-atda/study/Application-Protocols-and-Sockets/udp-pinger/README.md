# UDP Pinger

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Programming-Assignments/udp-pinger` |
| 정식 검증 | `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem test` |

## 한 줄 요약

UDP 비연결성과 timeout 기반 손실 처리를 RTT 측정 과제로 묶은 구현이다.

## 문제 요약

클라이언트가 10개의 ping 메시지를 보내고, 응답 도착 시간으로 RTT min/avg/max와 packet loss를 계산한다. 서버는 약 30% 패킷을 드롭한다.

## 이 프로젝트를 여기 둔 이유

웹 서버 다음 단계로, 연결 상태가 없는 전송에서 애플리케이션이 직접 timeout과 통계를 관리해야 함을 보여준다.

## 제공 자료

- `problem/code/udp_pinger_server.py` 제공 서버
- `problem/code/udp_pinger_client_skeleton.py` skeleton
- `problem/script/test_pinger.sh` 자동 검증

## 학습 포인트

- UDP의 connectionless socket 사용법
- timeout을 손실 판정으로 바꾸는 방법
- RTT 집계와 손실률 계산
- ICMP ping과 UDP echo 과제의 차이

## 실행과 검증

- 실행: `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 현재 범위와 한계

클라이언트 구현이 중심이다. 서버는 제공된 드롭 시뮬레이터를 그대로 사용한다.

- 현재 한계: 패킷 순서 역전은 별도 처리하지 않음
- 현재 한계: 분위수 통계 미지원
- 현재 한계: pytest는 서버 선기동 필요

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
