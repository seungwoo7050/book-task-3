# IP and ICMP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 IP/ICMP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 IP/ICMP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트
- 이 단계에서의 역할: 전송 계층 랩 다음에 네트워크 계층 헤더와 제어 메시지를 직접 읽으며, 이후 `ICMP Pinger`와 `Traceroute` 구현 프로젝트와 맞물리게 합니다.

## 제공된 자료
- `problem/data/ip-traceroute.pcapng`: traceroute 관련 IP/ICMP trace
- `problem/data/ip-fragmentation.pcapng`: fragmentation이 일어난 ICMP trace
- `analysis/src/ip-icmp-analysis.md`: 공개 답안

## 이 레포의 답
- 한 줄 답: IPv4 header, fragmentation, TTL, ICMP 메시지를 traceroute/ping 맥락에서 읽는 네트워크 계층 랩입니다.
- 공개 답안 위치: `analysis/src/`
- 보조 공개 표면: `docs/`
- 보조 공개 표면: `study/blog/03-Packet-Analysis-Top-Down/ip-icmp/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `analysis/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `../../blog/03-Packet-Analysis-Top-Down/ip-icmp/README.md` - 소스 기준의 분석 chronology를 따라갑니다.
  4. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.

## 어떻게 검증하나
- 검증: `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 무엇을 배웠나
- IPv4 header field 해석
- fragmentation 3요소(`Identification`, `Flags`, `Offset`)
- TTL과 traceroute 관계
- ICMP type/code 구분

## 현재 한계
- IPv4 중심이며 IPv6 비교는 개념 문서에서만 다룹니다.
- OS별 traceroute 구현 차이는 실험하지 않습니다.
