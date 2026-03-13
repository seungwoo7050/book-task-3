# DNS Packet Analysis evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 질문과 trace 범위를 먼저 세우기

- 당시 목표: `DNS Packet Analysis`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/dns/problem/README.md`, `study/03-Packet-Analysis-Top-Down/dns/problem/Makefile`, `study/03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`
- 무슨 판단을 했는가: 문제 설명보다 실행 표면을 먼저 잡아야 뒤 설명이 흔들리지 않는다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/dns/problem help
  open-nslookup          Open the nslookup trace in Wireshark GUI
  open-browsing          Open the web browsing DNS trace in Wireshark GUI
  filter-queries         Display all DNS query packets via tshark
  filter-responses       Display all DNS response packets via tshark
  filter-browsing        Display DNS queries triggered by web browsing
  summary                Print packet count summary for all traces
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: HTTP 다음 단계에서 이름 해석 계층을 관찰하며, 패킷 분석이 응용 계층 내부 프로토콜에도 그대로 적용된다는 점을 보여 줍니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`의 `## Part 1: nslookup`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. query/response 흐름과 권한 정보를 필드 단위로 확인하기

- 당시 목표: `DNS query/response 구조와 TTL 기반 캐시를 Wireshark로 해석하는 랩입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`
- 무슨 판단을 했는가: 중심 규칙은 넓게 흩어져 있지 않고, 실제 분기나 frame evidence가 모이는 지점에 있다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/dns/problem filter-queries
tshark -r data/dns-nslookup.pcapng -Y "dns.flags.response == 0" -T fields \
1	8.8.8.8	example.com	1
3	8.8.8.8	example.com	15
```
- 검증 신호:
  - 이 출력만으로도 `## Part 2: Authoritative and Non-Authoritative` 주변이 설명의 중심축이라는 점이 드러난다.
  - record type별 역할
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`의 `## Part 2: Authoritative and Non-Authoritative`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. verify 스크립트와 한계까지 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 검증 출력이 좋게 나와도 README limitation을 그대로 남겨야 범위가 정확해진다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/dns/problem test
PASS: dns answer file passed content verification
```
- 검증 신호:
  - `make -C study/03-Packet-Analysis-Top-Down/dns/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - 제공된 trace가 짧아 일부 질문은 관찰 불가로 남습니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`의 `## Part 3: DNS Responses and Records`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
