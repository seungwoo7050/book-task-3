# HTTP Packet Analysis development timeline

`HTTP Packet Analysis`를 읽을 때 먼저 잡아야 하는 것은 기능 목록이 아니라, 어디서부터 구현이나 분석이 무거워졌는가이다.

그래서 이 문서는 문제 문서, 핵심 파일, 테스트, CLI 출력만 남기고 나머지 군더더기는 걷어 냈다.

## 구현 순서 한눈에 보기

1. `study/03-Packet-Analysis-Top-Down/http/problem`의 문제 문서와 실행 target으로 출발점을 고정했다.
2. `study/03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`의 핵심 구간에서 동작 규칙을 설명할 수 있는 최소 앵커를 골랐다.
3. `make -C study/03-Packet-Analysis-Top-Down/http/problem test`와 테스트/verify 파일을 연결해 통과 신호와 남은 경계를 정리했다.

## 1. 질문과 trace 범위를 먼저 세우기

이 단계에서는 구현 세부로 바로 내려가지 않았다. 먼저 어떤 파일이 진입점이고 어떤 명령이 검증 기준인지 고정하는 일이 더 급했다.

- 당시 목표: `HTTP Packet Analysis`를 읽는 출발점과 성공 기준을 고정한다.
- 실제 진행: `problem/README.md`와 `problem/Makefile`을 먼저 확인한 뒤, `## Part 1: Basic HTTP GET / Response`가 있는 파일로 내려갔다.
- 검증 신호: `make help`에 보이는 target만으로도 이 프로젝트가 어떤 명령으로 열리고 닫히는지 설명할 수 있었다.
- 새로 배운 것: HTTP 상태 코드 해석

핵심 코드/trace:

```text
## Part 1: Basic HTTP GET / Response

**Trace file**: `http-basic.pcapng`

### Question 1

**Q: Is your browser running HTTP/1.0 or HTTP/1.1? What version of HTTP is the server running?**
```

왜 이 코드가 중요했는가:

문제 사양을 읽은 뒤 바로 이 지점으로 내려오면, 말로 적힌 요구가 실제 파일 구조와 어떻게 만나는지 곧바로 보인다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/http/problem help
  open-basic             Open the basic HTTP trace in Wireshark GUI
  open-conditional       Open the conditional GET trace in Wireshark GUI
  open-long              Open the long document trace in Wireshark GUI
  open-embedded          Open the embedded objects trace in Wireshark GUI
  filter-basic           Display HTTP packets from basic trace via tshark
  filter-conditional     Display HTTP packets from conditional trace via tshark
```

## 2. 기본 GET과 conditional GET을 frame 근거로 채우기

중간 단계의 핵심은 '무엇을 만들었나'보다 '어느 줄에서 규칙이 드러나는가'를 잡는 일이었다.

- 당시 목표: `기본 GET, conditional GET, 긴 문서 전송, embedded object 요청을 패킷 수준에서 추적하는 랩입니다.`를 실제 근거에 붙인다.
- 실제 진행: `## Part 2: Conditional GET` 주변을 중심으로 symbol이나 trace 결과를 다시 좁혀 읽었다.
- 검증 신호: 짧은 `rg`/filter 출력만으로도 어느 줄이 설명의 중심인지 바로 드러났다.
- 새로 배운 것: `If-Modified-Since`와 `304 Not Modified`

핵심 코드/trace:

```text
## Part 2: Conditional GET

**Trace file**: `http-conditional.pcapng`

### Question 8

**Q: Inspect the first HTTP GET request. Is there an If-Modified-Since header? What about If-None-Match?**
```

왜 이 코드가 중요했는가:

핵심은 함수 이름 자체가 아니라, 이 줄 주변에서 어떤 입력이 어떤 결과로 바뀌는지가 한 번에 드러난다는 점이다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/http/problem filter-basic
tshark -r data/http-basic.pcapng -Y "http" -T fields \
4	192.168.0.2	128.119.245.12	GET	/kurose_ross_small/HTTP/index.html
6	128.119.245.12	192.168.0.2		/kurose_ross_small/HTTP/index.html	200	36
```

## 3. verify 스크립트와 한계까지 정리하기

마지막 단계에서는 단순히 테스트가 통과했다는 사실만 적지 않으려고 했다. 어디까지 확인됐고 무엇이 아직 범위 밖인지 같이 남겨야 글이 정직해진다.

- 당시 목표: 검증 결과와 남은 경계를 함께 정리한다.
- 실제 진행: `make -C study/03-Packet-Analysis-Top-Down/http/problem test`를 다시 실행하고, `## Part 3: Long Documents`가 남아 있는 파일을 본문 마지막 근거로 삼았다.
- 검증 신호: 현재 공개 답안이 재현된다는 출력과, README limitation이 동시에 확인됐다.
- 새로 배운 것: 긴 응답이 여러 TCP segment로 나뉘는 모습

핵심 코드/trace:

```text
## Part 3: Long Documents

**Trace file**: `http-long-document.pcapng`

### Question 12

**Q: How many HTTP GET requests did your browser send? How many TCP segments were needed to carry the single HTTP response?**
```

왜 이 코드가 중요했는가:

마지막에 이 파일을 남겨 두는 이유는, 이 프로젝트가 실제로 무엇을 통과해야 끝나는지 가장 직접적으로 보여 주기 때문이다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/http/problem test
PASS: http answer file passed content verification
```

## 남은 경계

- `HTTP/2` 이상은 다루지 않습니다.
- 브라우저별 헤더 차이는 관찰 범위 밖입니다.
- 실시간 캡처 대신 고정 trace에 기반합니다.
