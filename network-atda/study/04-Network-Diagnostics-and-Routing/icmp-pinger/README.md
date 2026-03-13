# ICMP Pinger

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 ICMP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
| 정식 검증 | `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 ICMP ping 과제를 현재 저장소 구조에 맞게 정리한 프로젝트
- 이 단계에서의 역할: 응용 계층 소켓 과제보다 한 단계 아래로 내려가 IP/ICMP 레벨에서 무엇이 직접 보이는지 체감하게 합니다.

## 제공된 자료
- `problem/code/icmp_pinger_skeleton.py`: 시작용 skeleton 코드
- `problem/script/test_icmp.sh`: live raw-socket 검증 스크립트
- `python/tests/test_icmp_pinger.py`: 비권한 deterministic 테스트

## 이 레포의 답
- 한 줄 답: Raw socket으로 `ICMP Echo Request/Reply`를 직접 구현하는 진단 도구 과제입니다.
- 공개 답안 위치: `python/src/`
- 보조 공개 표면: `python/tests/`
- 보조 공개 표면: `docs/`
- 보조 공개 표면: `study/blog/04-Network-Diagnostics-and-Routing/icmp-pinger/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `python/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `../../blog/04-Network-Diagnostics-and-Routing/icmp-pinger/README.md` - 실제 소스 기준의 개발 chronology를 따라갑니다.
  4. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.
  5. `notion/README.md` - 공개 학습 노트이지만 엔트리포인트는 아닙니다.

## 어떻게 검증하나
- 실행: `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem run-solution HOST=google.com`
- 검증: `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- 수동 live 검증: `sudo make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test-live HOST=google.com`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 무엇을 배웠나
- RFC 1071 인터넷 체크섬
- raw socket 권한 모델
- IP header length(`IHL`) 파싱
- binary packet build/parse 패턴
- fake-socket 기반 deterministic integration test 설계

## 현재 한계
- IPv6/ICMPv6는 지원하지 않습니다.
- 시스템 `ping` 수준의 상세 통계는 제공하지 않습니다.
- live raw-socket 실행은 OS와 방화벽 정책에 영향을 받습니다.
