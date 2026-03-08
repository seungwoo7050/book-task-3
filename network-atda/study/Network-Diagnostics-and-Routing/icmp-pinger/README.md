# ICMP Pinger

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Programming-Assignments/icmp-pinger` |
| 정식 검증 | `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test` |

## 한 줄 요약

Raw socket으로 ICMP Echo Request/Reply를 직접 구현하는 진단 도구 과제다.

## 문제 요약

ICMP 패킷을 직접 만들고 수신 패킷에서 IP 헤더를 넘겨 ICMP Echo Reply를 파싱한 뒤 RTT와 packet loss를 출력한다.

## 이 프로젝트를 여기 둔 이유

응용 계층 소켓 과제보다 한 단계 아래로 내려가 IP/ICMP 레벨에서 무엇이 직접 보여지는지 체감하게 한다.

## 제공 자료

- `problem/code/icmp_pinger_skeleton.py` skeleton
- `problem/script/test_icmp.sh` live raw-socket 검증 스크립트
- `python/tests/test_icmp_pinger.py` 비권한 deterministic tests

## 학습 포인트

- RFC 1071 인터넷 체크섬
- raw socket 권한 모델
- IP header length(IHL) 파싱
- binary packet build/parse 패턴
- deterministic fake-socket integration test 설계

## 실행과 검증

- 실행: `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem run-solution HOST=google.com`
- 검증: `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test`
- 수동 live 검증: `sudo make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test-live HOST=google.com`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 현재 범위와 한계

비권한 deterministic test가 checksum, packet build, reply parsing, RTT/statistics 출력 흐름까지 검증한다. live raw-socket 실행은 수동 재현 경로로 남긴다.

- 현재 한계: IPv6/ICMPv6 미지원
- 현재 한계: 시스템 ping 수준의 상세 통계 미지원
- 현재 한계: live raw-socket 실행은 OS/방화벽 정책에 영향받음

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
