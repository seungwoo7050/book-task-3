# UDP Pinger

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 UDP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem test` |

## 한 줄 요약

UDP의 비연결성과 timeout 기반 손실 처리를 RTT 측정 과제로 묶은 구현입니다.

## 왜 이 프로젝트가 필요한가

웹 서버 다음 단계에서 "연결이 없는 전송"이 애플리케이션 코드에 어떤 책임을 남기는지 분명하게 드러냅니다.

## 이런 학습자에게 맞습니다

- TCP와 달리 손실 판정과 통계를 직접 계산해야 하는 이유를 보고 싶은 학습자
- socket timeout과 RTT 계산을 실전 예제로 익히고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 구현 목표, 제공 자료, 성공 기준을 먼저 확인합니다.
2. `python/README.md` - 공개 구현 범위와 정식 검증 명령을 확인합니다.
3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
4. `notion/README.md` - 더 깊은 작업 기록과 회고가 필요할 때 참고합니다.

## 제공 자료

- `problem/code/udp_pinger_server.py`: 손실을 시뮬레이션하는 제공 서버
- `problem/code/udp_pinger_client_skeleton.py`: 클라이언트 skeleton
- `problem/script/test_pinger.sh`: 정식 검증 스크립트

## 실행과 검증

- 실행: `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem run-solution`
- 검증: `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 학습 포인트

- UDP의 connectionless socket 사용법
- 1초 timeout을 손실 판정으로 바꾸는 방법
- RTT 최소값/평균값/최대값과 손실률 계산
- ICMP ping과 UDP echo 과제의 차이 이해

## 현재 한계

- 패킷 순서 역전은 별도 처리하지 않습니다.
- 분위수 같은 고급 통계는 계산하지 않습니다.
- `pytest` 단독 실행은 제공 서버 선기동이 필요합니다.

## 포트폴리오로 확장하기

- RTT 분포 그래프, percentile 통계, CLI 옵션을 추가하면 단순 과제 구현에서 도구형 프로젝트로 확장됩니다.
- 손실률이 바뀌는 서버 조건에서 결과가 어떻게 달라지는지 표로 정리하면 학습 깊이가 드러납니다.
- ICMP ping 과제와 비교한 차이를 README에 명시하면 같은 저장소 안의 연결성이 좋아집니다.
