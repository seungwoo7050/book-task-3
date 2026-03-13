# Ethernet and ARP Packet Analysis 개발 타임라인

## Day 1 — 세 frame만으로 링크 계층을 읽기

### Session 1

- 목표: 가장 먼저 broadcast와 unicast를 Ethernet destination으로 구분한다.
- 진행: `filter-broadcast`와 `filter-arp`를 같이 봤다. frame 1은 `ff:ff:ff:ff:ff:ff`로 향하고, frame 2는 `00:11:22:33:44:55`로 되돌아온다. 같은 ARP라도 request와 reply의 전송 방식이 다르다는 점이 바로 보였다.
- 이슈: 처음에는 ARP를 IP를 보조하는 부속품 정도로 생각했다. 그런데 이 trace는 오히려 링크 계층 관점이 더 중요했다. destination MAC만 봐도 packet의 의도가 거의 드러났다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem filter-broadcast
1   00:11:22:33:44:55   0x0806
```

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem filter-arp
1   00:11:22:33:44:55   ff:ff:ff:ff:ff:ff   1   00:11:22:33:44:55   192.168.0.2   00:00:00:00:00:00   192.168.0.1
2   66:77:88:99:aa:bb   00:11:22:33:44:55   2   66:77:88:99:aa:bb   192.168.0.1   00:11:22:33:44:55   192.168.0.2
```

- 메모: 여기서 `opcode 1`, target MAC `00:00:00:00:00:00`, broadcast destination이 request를 설명하고, `opcode 2`, known MAC, unicast destination이 reply를 설명한다는 그림이 한 번에 잡혔다.

### Session 2

- 목표: EtherType과 다음 frame을 연결해 address resolution 이후 실제 데이터 전송이 이어지는지 본다.
- 진행: `filter-ethernet`을 보니 frame 1과 2는 `0x0806`, frame 3은 `0x0800`이다. 즉 ARP 두 frame 뒤에 IPv4 frame이 바로 붙는다. frame 3의 destination MAC은 방금 ARP reply에서 배운 `66:77:88:99:aa:bb`다.
- 이슈: trace가 너무 짧아서 더 많은 예시를 찾고 싶었다. 하지만 오히려 이 최소 구성 덕분에 "ARP로 MAC을 알아내고, 다음 L3 packet이 그 MAC을 사용한다"는 핵심 흐름이 흐려지지 않았다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem filter-ethernet
1   00:11:22:33:44:55   ff:ff:ff:ff:ff:ff   0x0806
2   66:77:88:99:aa:bb   00:11:22:33:44:55   0x0806
3   00:11:22:33:44:55   66:77:88:99:aa:bb   0x0800
```

- 메모: frame 3 하나만으로도 ARP가 "질문/답변으로 끝나는 프로토콜"이 아니라 이후 IP 전송을 준비하는 단계라는 점이 분명해졌다.

### Session 3

- 목표: trace에 없는 상위 계층 packet을 어떻게 다룰지 기준을 세운다.
- 진행: analysis 문서를 다시 보니 HTTP GET의 바이트 오프셋을 묻는 교재 질문이 있었지만, 이 trace에는 HTTP packet이 없다. 그래서 없는 packet을 억지로 찾는 대신, `http.request` filter가 zero frame이라는 점 자체를 evidence로 채택했다.
- 이슈: 이런 경우 일반적인 네트워크 지식을 길게 적고 싶어진다. 하지만 그 순간 이 글은 capture 해설이 아니라 추측으로 변한다.

CLI:

```bash
$ make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test
bash script/verify_answers.sh
Ethernet/ARP analysis answers look complete.
```

- 정리:
	- ARP request와 reply는 opcode보다 먼저 destination MAC에서 성격이 갈렸다.
	- EtherType `0x0806`과 `0x0800`의 전환이 주소 해석 이후 실제 전송 개시를 보여 줬다.
	- 없는 HTTP packet을 억지로 보충하지 않고, trace의 빈칸을 그대로 남기는 편이 더 정확했다.
