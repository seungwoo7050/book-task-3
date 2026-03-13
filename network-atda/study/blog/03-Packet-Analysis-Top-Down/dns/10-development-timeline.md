# DNS Packet Analysis 개발 타임라인

## Day 1 — query/response 짝을 먼저 세우기

### Session 1

- 목표: DNS를 결과표처럼 읽지 않고, query와 response를 한 쌍으로 묶는 기준부터 만든다.
- 진행: `dns-nslookup.pcapng`에서 query만 먼저 뽑았다. `example.com`에 대해 A 질의와 MX 질의가 각각 따로 나간다. 둘 다 UDP 53으로 향한다.
- 이슈: 처음엔 `example.com -> 93.184.216.34`처럼 결과 한 줄만 적으면 된다고 생각했다. 하지만 이 방식으로는 A 질의인지 MX 질의인지, 누가 resolver인지, answer count가 몇 개인지 남지 않는다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/dns/problem filter-queries
1   8.8.8.8   example.com   A
3   8.8.8.8   example.com   MX
```

- 메모: 이 출력 덕분에 "질문 종류가 둘이다"를 초반에 고정했다. 이후 response를 읽을 때도 frame 2는 A 응답, frame 4는 MX 응답이라는 기준이 흔들리지 않았다.

### Session 2

- 목표: response를 읽으면서 answer count, TTL, authoritative 여부를 구분한다.
- 진행: `filter-responses`로 기본 응답 필드를 먼저 확인한 뒤, Wireshark frame detail에서 authoritative bit를 따로 확인했다. frame 2는 authoritative, frame 4는 non-authoritative였다.
- 이슈: `8.8.8.8`을 보고 곧바로 "내 기본 DNS 서버다"라고 쓰고 싶었지만, trace만으로는 거기까지 단정할 수 없다. 이 capture는 단지 질의가 8.8.8.8로 갔다는 사실만 보여 준다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/dns/problem filter-responses
2   example.com   A    93.184.216.34         300
4   example.com   MX                         300
```

- 메모: frame 4에서 MX 타입과 TTL은 보이는데, 교환기 이름과 preference는 깔끔하게 디코딩되지 않았다. 여기서 처음으로 "보이는 필드만 답으로 삼자"는 기준이 확실해졌다.

### Session 3

- 목표: malformed response와 너무 짧은 browsing trace를 어떻게 처리할지 정한다.
- 진행: frame 4를 다시 보니 `Type: MX (15)` 뒤에 `[Malformed Packet: DNS]`가 붙어 있었다. 이어서 `dns-web-browsing.pcapng`를 보니 packet이 단 두 개뿐이었다. query 1개, response 1개다.
- 이슈: 교재 질문을 다 채우려는 욕심 때문에, TCP SYN 목적지나 캐시된 다음 응답 TTL 변화까지 추정하고 싶었다. 하지만 이 trace에는 TCP packet 자체가 없고, `www.ietf.org`에 대한 response도 한 번뿐이다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/dns/problem filter-browsing
1   0   www.ietf.org   A
2   1   www.ietf.org   A
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/dns/problem test
bash script/verify_answers.sh
DNS analysis answers look complete.
```

- 정리:
	- DNS 답안의 기본 단위는 "질의 한 개, 응답 한 개"였다.
	- resolver 주소, authoritative bit, TTL은 각각 trace가 허용하는 수준까지만 말해야 했다.
	- malformed response는 빈칸을 억지로 채우는 대신, 디코더가 멈춘 지점을 evidence로 남기는 편이 더 정확했다.
	- 짧은 browsing trace는 "모르는 것까지 적지 않는 훈련"에 오히려 더 도움이 됐다.
