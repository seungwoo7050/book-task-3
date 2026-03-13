# DNS Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 DNS Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/dns/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 DNS Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트
- 이 단계에서의 역할: HTTP 다음 단계에서 이름 해석 계층을 관찰하며, 패킷 분석이 응용 계층 내부 프로토콜에도 그대로 적용된다는 점을 보여 줍니다.

## 제공된 자료
- `problem/data/dns-nslookup.pcapng`: `nslookup`/`dig` 계열 질의 trace
- `problem/data/dns-web-browsing.pcapng`: 웹 브라우징 중 발생한 DNS trace
- `analysis/src/dns-analysis.md`: 공개 답안

## 이 레포의 답
- 한 줄 답: DNS query/response 구조와 TTL 기반 캐시를 Wireshark로 해석하는 랩입니다.
- 공개 답안 위치: `analysis/src/`
- 보조 공개 표면: `docs/`
- 보조 공개 표면: `study/blog/03-Packet-Analysis-Top-Down/dns/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `analysis/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `../../blog/03-Packet-Analysis-Top-Down/dns/README.md` - 소스 기준의 분석 chronology를 따라갑니다.
  4. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.

## 어떻게 검증하나
- 검증: `make -C study/03-Packet-Analysis-Top-Down/dns/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 무엇을 배웠나
- DNS header/question/answer 구조
- record type별 역할
- recursive resolution과 authoritative/non-authoritative 차이
- TTL 감소와 cache hit 해석

## 현재 한계
- 제공된 trace가 짧아 일부 질문은 관찰 불가로 남습니다.
- 권한 서버 위임 체인을 완전히 재현하는 trace는 아닙니다.
- 일부 응답은 malformed 상태라 field 해석이 제한됩니다.
