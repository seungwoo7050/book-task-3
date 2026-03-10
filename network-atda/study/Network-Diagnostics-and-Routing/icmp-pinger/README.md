# ICMP Pinger

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 ICMP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test` |

## 한 줄 요약

Raw socket으로 `ICMP Echo Request/Reply`를 직접 구현하는 진단 도구 과제입니다.

## 왜 이 프로젝트가 필요한가

응용 계층 소켓 과제보다 한 단계 아래로 내려가 IP/ICMP 레벨에서 무엇이 직접 보이는지 체감하게 합니다.

## 이런 학습자에게 맞습니다

- raw socket과 IP 헤더 파싱을 직접 경험해 보고 싶은 학습자
- 권한이 필요한 live 실행과 비권한 deterministic test를 구분해 보고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 구현 목표, 제공 자료, 성공 기준을 먼저 확인합니다.
2. `python/README.md` - 공개 구현 범위와 정식 검증 명령을 확인합니다.
3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
4. `notion/README.md` - 더 깊은 작업 기록과 회고가 필요할 때 참고합니다.

## 제공 자료

- `problem/code/icmp_pinger_skeleton.py`: 시작용 skeleton 코드
- `problem/script/test_icmp.sh`: live raw-socket 검증 스크립트
- `python/tests/test_icmp_pinger.py`: 비권한 deterministic 테스트

## 실행과 검증

- 실행: `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem run-solution HOST=google.com`
- 검증: `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- 수동 live 검증: `sudo make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test-live HOST=google.com`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 학습 포인트

- RFC 1071 인터넷 체크섬
- raw socket 권한 모델
- IP header length(`IHL`) 파싱
- binary packet build/parse 패턴
- fake-socket 기반 deterministic integration test 설계

## 현재 한계

- IPv6/ICMPv6는 지원하지 않습니다.
- 시스템 `ping` 수준의 상세 통계는 제공하지 않습니다.
- live raw-socket 실행은 OS와 방화벽 정책에 영향을 받습니다.

## 포트폴리오로 확장하기

- `IPv6`, `TTL`, `패킷 크기` 옵션을 추가하면 도구형 프로젝트로 확장하기 좋습니다.
- 권한이 필요한 live 실행과 비권한 테스트를 분리한 이유를 문서로 설명하면 성숙한 설계 판단으로 보입니다.
- 운영체제별 raw socket 제약을 비교 표로 정리하면 학습 깊이가 잘 드러납니다.
