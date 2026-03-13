# TLS Packet Analysis evidence ledger

이 문서는 긴 본문을 읽기 전에, 세 단계에서 어떤 판단이 있었는지만 빠르게 붙들기 위한 압축본이다.

## Phase 1. 질문과 trace 범위를 먼저 세우기

- 당시 목표: `TLS Packet Analysis`를 어디서부터 읽어야 하는지 고정한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/tls-ssl/problem/README.md`, `study/03-Packet-Analysis-Top-Down/tls-ssl/problem/Makefile`, `study/03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`
- 무슨 판단을 했는가: 어디서 실행하고 어디서 검증하는지 먼저 정하지 않으면 본문이 기능 요약으로 흘러갈 가능성이 컸다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem help
  open           - Open trace file in Wireshark
  handshake      - Filter all TLS handshake messages
  client-hello   - Filter ClientHello messages
  server-hello   - Filter ServerHello messages
  certs          - Filter Certificate messages
  cipher-change  - Filter ChangeCipherSpec messages
```
- 검증 신호:
  - `make help`만 봐도 이 프로젝트가 어떤 target으로 열리고 닫히는지 드러난다.
  - 이 단계에서의 역할: top-down 순서의 마지막에서 보안 프로토콜이 transport 위에 어떻게 올라가는지 정리하며, 암호화 이후 무엇이 보이고 무엇이 보이지 않는지도 함께 보여 줍니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`의 `## Part 1: ClientHello (Q1–Q5)`
- 다음으로 넘어간 이유: 이제 어디를 읽어야 할지 정해졌으니, 실제로 판단이 몰린 함수나 trace section으로 내려갈 수 있었다.

## Phase 2. ClientHello와 ServerHello/Certificate를 handshake 축으로 묶기

- 당시 목표: `TLS handshake, certificate, cipher suite, 버전 차이를 record/message 수준에서 읽는 보안 랩입니다.`를 실제 코드나 trace 근거에 붙여 본다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`
- 무슨 판단을 했는가: 전체 파일을 다 설명하기보다, 판단이 바뀐 줄 몇 개를 먼저 붙드는 편이 더 정확하다고 판단했다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem handshake
tshark -r data/tls-trace.pcap -Y "tls.handshake" \
4	192.168.0.2	93.184.216.34	1
5	93.184.216.34	192.168.0.2	2,11
```
- 검증 신호:
  - 이 출력만으로도 `## Part 2: ServerHello and Certificate (Q6–Q11)` 주변이 설명의 중심축이라는 점이 드러난다.
  - cipher suite 의미
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`의 `## Part 2: ServerHello and Certificate (Q6–Q11)`
- 다음으로 넘어간 이유: 중심 규칙을 잡은 뒤에는, 이 구현이나 분석이 실제로 무엇으로 닫히는지만 확인하면 됐다.

## Phase 3. verify 스크립트와 한계까지 정리하기

- 당시 목표: 통과 신호와 남은 범위를 한 번에 정리한다.
- 핵심 변경 단위: `study/03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`, `problem/script/`, `docs/`
- 무슨 판단을 했는가: 테스트 통과만 적으면 과장이 되기 쉬워서, 어디까지 확인됐고 무엇이 남는지도 같이 적어야 한다고 봤다.
- 실행한 CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test
PASS: tls-ssl answer file passed content verification
```
- 검증 신호:
  - `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test`가 현재 공개 답안을 다시 재현해 준다.
  - 제공 trace가 minimal synthetic capture라 일부 certificate detail과 extension은 제한적입니다.
- 핵심 코드/trace 앵커: `study/03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`의 `## Part 3: ChangeCipherSpec and Application Data (Q12–Q16)`
- 다음으로 넘어간 이유: 통과 신호와 경계가 모두 적혔으니, 긴 본문에서는 각 단계를 더 사람 읽기 좋게 풀어 쓰면 된다.
