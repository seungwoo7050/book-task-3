# UDP Pinger

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 UDP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 UDP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트
- 이 단계에서의 역할: 웹 서버 다음 단계에서 "연결이 없는 전송"이 애플리케이션 코드에 어떤 책임을 남기는지 분명하게 드러냅니다.

## 제공된 자료
- `problem/code/udp_pinger_server.py`: 손실을 시뮬레이션하는 제공 서버
- `problem/code/udp_pinger_client_skeleton.py`: 클라이언트 skeleton
- `problem/script/test_pinger.sh`: 정식 검증 스크립트

## 이 레포의 답
- 한 줄 답: UDP의 비연결성과 timeout 기반 손실 처리를 RTT 측정 과제로 묶은 구현입니다.
- 공개 답안 위치: `python/src/`
- 보조 공개 표면: `python/tests/`
- 보조 공개 표면: `docs/`
- 보조 공개 표면: `study/blog/01-Application-Protocols-and-Sockets/udp-pinger/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `python/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `../../blog/01-Application-Protocols-and-Sockets/udp-pinger/README.md` - 실제 소스 기준의 개발 chronology를 따라갑니다.
  4. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
  5. `notion/README.md` - 공개 학습 노트이지만 엔트리포인트는 아닙니다.

## 어떻게 검증하나
- 실행: `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem run-solution`
- 검증: `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 무엇을 배웠나
- UDP의 connectionless socket 사용법
- 1초 timeout을 손실 판정으로 바꾸는 방법
- RTT 최소값/평균값/최대값과 손실률 계산
- ICMP ping과 UDP echo 과제의 차이 이해

## 현재 한계
- 패킷 순서 역전은 별도 처리하지 않습니다.
- 분위수 같은 고급 통계는 계산하지 않습니다.
- `pytest` 단독 실행은 제공 서버 선기동이 필요합니다.
