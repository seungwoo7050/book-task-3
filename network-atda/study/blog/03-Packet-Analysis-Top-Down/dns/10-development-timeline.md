# DNS Packet Analysis development timeline

`DNS Packet Analysis`를 읽을 때 먼저 잡아야 하는 것은 기능 목록이 아니라, 어디서부터 구현이나 분석이 무거워졌는가이다.

그래서 이 문서는 문제 문서, 핵심 파일, 테스트, CLI 출력만 남기고 나머지 군더더기는 걷어 냈다.

## 구현 순서 한눈에 보기

1. `study/03-Packet-Analysis-Top-Down/dns/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/03-Packet-Analysis-Top-Down/dns/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 질문과 trace 범위를 먼저 세우기

이 단계에서는 구현 세부로 바로 내려가지 않았다. 먼저 어떤 파일이 진입점이고 어떤 명령이 검증 기준인지 고정하는 일이 더 급했다.

- 당시 목표: `DNS Packet Analysis`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `## Part 1: nslookup`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: DNS header/question/answer 구조

핵심 코드/trace:

```text
## Part 1: nslookup

**Trace file**: `dns-nslookup.pcapng`

### Question 1

**Q: What transport-layer protocol is used by DNS? What port number does the DNS server listen on?**
```

왜 이 코드가 중요했는가:

문제 사양을 읽은 뒤 바로 이 지점으로 내려오면, 말로 적힌 요구가 실제 파일 구조와 어떻게 만나는지 곧바로 보인다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/dns/problem help
  open-nslookup          Open the nslookup trace in Wireshark GUI
  open-browsing          Open the web browsing DNS trace in Wireshark GUI
  filter-queries         Display all DNS query packets via tshark
  filter-responses       Display all DNS response packets via tshark
  filter-browsing        Display DNS queries triggered by web browsing
  summary                Print packet count summary for all traces
```

## 2. query/response 흐름과 권한 정보를 필드 단위로 확인하기

중간 단계의 핵심은 '무엇을 만들었나'보다 '어느 줄에서 규칙이 드러나는가'를 잡는 일이었다.

- 당시 목표: `DNS query/response 구조와 TTL 기반 캐시를 Wireshark로 해석하는 랩입니다.`를 실제 근거에 붙인다.
- 실제 진행: `## Part 2: Authoritative and Non-Authoritative` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: record type별 역할

핵심 코드/trace:

```text
## Part 2: Authoritative and Non-Authoritative

### Question 7

**Q: To what IP address is the DNS query sent? Is this the default local DNS server?**

**A:** The observed DNS queries are sent to **8.8.8.8** (frames #1 and #3).
```

왜 이 코드가 중요했는가:

핵심은 함수 이름 자체가 아니라, 이 줄 주변에서 어떤 입력이 어떤 결과로 바뀌는지가 한 번에 드러난다는 점이다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/dns/problem filter-queries
tshark -r data/dns-nslookup.pcapng -Y "dns.flags.response == 0" -T fields \
1	8.8.8.8	example.com	1
3	8.8.8.8	example.com	15
```

## 3. verify 스크립트와 한계까지 정리하기

마지막 단계에서는 단순히 테스트가 통과했다는 사실만 적지 않으려고 했다. 어디까지 확인됐고 무엇이 아직 범위 밖인지 같이 남겨야 글이 정직해진다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/03-Packet-Analysis-Top-Down/dns/problem test`를 다시 실행하고, `## Part 3: DNS Responses and Records`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: recursive resolution과 authoritative/non-authoritative 차이

핵심 코드/trace:

```text
# DNS Lab — Analysis Answers

## Trace Limitations

- This report uses only the repository-provided trace files.
- If a worksheet item needs packets that are not present in these traces, the answer is marked as `Not observable in this provided trace`.
- Missing values are not guessed; only decoded packet evidence is used.
- Numeric claims are tied to explicit frame references.
```

왜 이 코드가 중요했는가:

마지막에 이 파일을 남겨 두는 이유는, 이 프로젝트가 실제로 무엇을 통과해야 끝나는지 가장 직접적으로 보여 주기 때문이다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/dns/problem test
PASS: dns answer file passed content verification
```

## 남은 경계

- 제공된 trace가 짧아 일부 질문은 관찰 불가로 남습니다.
- 권한 서버 위임 체인을 완전히 재현하는 trace는 아닙니다.
- 일부 응답은 malformed 상태라 field 해석이 제한됩니다.
