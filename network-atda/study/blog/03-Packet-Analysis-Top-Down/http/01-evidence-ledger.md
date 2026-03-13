# HTTP Packet Analysis evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 질문과 trace 범위를 먼저 세우기

- 당시 목표: `HTTP Packet Analysis`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/http/problem/README.md`, `study/03-Packet-Analysis-Top-Down/http/problem/Makefile`, `study/03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`
- 무슨 판단을 했는가: 문제 설명보다 실행 표면을 먼저 잡아야 뒤 설명이 흔들리지 않는다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/http/problem help
  open-basic             Open the basic HTTP trace in Wireshark GUI
  open-conditional       Open the conditional GET trace in Wireshark GUI
  open-long              Open the long document trace in Wireshark GUI
  open-embedded          Open the embedded objects trace in Wireshark GUI
  filter-basic           Display HTTP packets from basic trace via tshark
  filter-conditional     Display HTTP packets from conditional trace via tshark
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: 사람이 읽을 수 있는 텍스트 프로토콜인 HTTP를 시작점으로 삼아, Wireshark로 무엇을 관찰하고 어떤 근거로 설명해야 하는지 감을 잡기 좋습니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`의 `## Part 1: Basic HTTP GET / Response`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. 기본 GET과 conditional GET을 frame 근거로 채우기

- 당시 목표: `기본 GET, conditional GET, 긴 문서 전송, embedded object 요청을 패킷 수준에서 추적하는 랩입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`
- 무슨 판단을 했는가: 중심 규칙은 넓게 흩어져 있지 않고, 실제 분기나 frame evidence가 모이는 지점에 있다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/http/problem filter-basic
tshark -r data/http-basic.pcapng -Y "http" -T fields \
4	192.168.0.2	128.119.245.12	GET	/kurose_ross_small/HTTP/index.html
6	128.119.245.12	192.168.0.2		/kurose_ross_small/HTTP/index.html	200	36
```
- 검증 신호:
  - 이 출력만으로도 `## Part 2: Conditional GET` 주변이 설명의 중심축이라는 점이 드러난다.
  - `If-Modified-Since`와 `304 Not Modified`
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`의 `## Part 2: Conditional GET`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. verify 스크립트와 한계까지 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 검증 출력이 좋게 나와도 README limitation을 그대로 남겨야 범위가 정확해진다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/http/problem test
PASS: http answer file passed content verification
```
- 검증 신호:
  - `make -C study/03-Packet-Analysis-Top-Down/http/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - `HTTP/2` 이상은 다루지 않습니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`의 `## Part 3: Long Documents`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
