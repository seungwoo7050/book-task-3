# IP and ICMP Packet Analysis 개발 타임라인

## Day 1 — traceroute와 fragmentation을 따로 읽기 시작

### Session 1

- 목표: traceroute trace에서 TTL이 hop 수를 어떻게 드러내는지 확인한다.
- 진행: 먼저 Echo Request만 뽑았다. frame 1, 3, 5의 TTL이 1, 2, 3으로 차례로 올라간다. `ip.id`도 `0x0fa0`, `0x0fa1`, `0x0fa2`로 함께 증가한다.
- 이슈: 처음에는 `ICMP Type 11`만 찾으면 traceroute 설명이 끝날 줄 알았다. 하지만 그렇게 보면 왜 다른 router가 차례로 응답하는지, probe마다 무엇이 달라지는지 설명이 비어 버린다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem filter-ttl
1   1   0x0fa0   93.184.216.34
3   2   0x0fa1   93.184.216.34
5   3   0x0fa2   93.184.216.34
```

- 메모: TTL과 `ip.id`를 같이 보니 traceroute probe가 정말 서로 다른 IP datagram이라는 점이 감각적으로 들어왔다.

### Session 2

- 목표: router가 보내는 ICMP 응답을 probe와 짝지어 읽는다.
- 진행: `filter-icmp`로 request와 response를 한 번에 뽑고, 어떤 source IP가 어떤 TTL에서 등장하는지 확인했다. frame 2는 `10.0.0.1`, frame 4는 `172.16.0.1`에서 온 `Type 11 / Code 0`이다. 마지막 frame 6만 `Echo Reply`다.
- 이슈: 처음에는 ICMP를 하나의 프로토콜로만 보고 Echo Reply와 Time Exceeded를 같은 성격의 응답처럼 취급할 뻔했다. 실제로는 traceroute에서 중요한 건 오류 메시지가 아니라 "TTL이 다 떨어졌다는 사실을 중간 router가 대신 알려 준다"는 구조였다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem filter-icmp
1   10.0.0.2       93.184.216.34   1    8    0   0x0fa0
2   10.0.0.1       10.0.0.2       64   11   0   0x2000
3   10.0.0.2       93.184.216.34   2    8    0   0x0fa1
4   172.16.0.1     10.0.0.2       64   11   0   0x2001
5   10.0.0.2       93.184.216.34   3    8    0   0x0fa2
6   93.184.216.34  10.0.0.2       64   0    0   0x3000
```

- 메모: 이 출력 덕분에 traceroute를 "TTL 실험 + router 보고"로 설명할 수 있게 됐다. 단순히 ICMP 종류를 외우는 것과는 느낌이 달랐다.

### Session 3

- 목표: fragmentation trace를 별도의 문제로 읽고, reassembly 책임이 어디에 있는지 정리한다.
- 진행: `filter-fragments`를 돌리니 세 fragment가 같은 `ip.id=0x3039`를 공유하고, offset이 0, 175, 350으로 이어졌다. 마지막 fragment만 `MF=0`이다. Wireshark는 final fragment에서 reassembly metadata를 보여 준다.
- 이슈: 처음엔 fragment 개수만 세면 설명이 끝난다고 생각했다. 그런데 offset이 8-byte 단위라는 점과 마지막 fragment만 `MF=0`이라는 점을 빼면, 왜 이 셋이 한 datagram인지 설명이 약해진다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem filter-fragments
1   0x3039   1   0     1420
2   0x3039   1   175   1420
3   0x3039   0   350   728
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test
bash script/verify_answers.sh
IP/ICMP analysis answers look complete.
```

- 정리:
	- traceroute는 ICMP 메시지 이름보다 TTL 변화와 router source IP 대응이 더 중요했다.
	- `ip.id`는 독립된 probe와 fragment 묶음을 추적하는 실마리로 계속 등장했다.
	- fragmentation 설명은 개수 세기보다 `MF`, `frag_offset`, final fragment의 reassembly metadata를 같이 보는 편이 정확했다.
