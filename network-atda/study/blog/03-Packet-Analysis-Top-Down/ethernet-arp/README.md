# Ethernet and ARP Packet Analysis Blog

이 문서 묶음은 `ethernet-arp`를 "링크 계층 이론 요약"이 아니라 "3개의 frame만으로 IP 주소가 MAC 주소로 연결되는 순간을 어디까지 설명할 수 있는가"라는 질문으로 다시 읽는다. 현재 답안은 broadcast ARP request, unicast ARP reply, 그 직후 IPv4 frame이라는 최소 3-frame sequence만을 근거로 한다. 따라서 이 lab의 핵심은 풍부한 trace를 다루는 것이 아니라, 작은 trace에서도 주소 해석의 문턱이 무엇인지 정확히 짚는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/03-Packet-Analysis-Top-Down/ethernet-arp/problem/README.md`
- 답안 경계: `README.md`, `analysis/README.md`, `analysis/src/ethernet-arp-analysis.md`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test`
- 보조 필터: `make -C .../ethernet-arp/problem filter-arp`, `filter-ethernet`, `filter-broadcast`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test`
- 결과: `PASS: ethernet-arp answer file passed content verification`
- 보조 필터에서 재확인한 값:
  - frame `1`: broadcast ARP request, target IP `192.168.0.1`
  - frame `2`: unicast ARP reply, sender MAC `66:77:88:99:aa:bb`
  - frame `3`: IPv4 frame destination MAC `66:77:88:99:aa:bb`

## 지금 남기는 한계

- trace가 3 frame뿐이라 HTTP GET offset이나 ARP spoofing 사례는 관찰할 수 없다.
- ARP cache timeout은 일반론으로 설명할 수는 있어도 trace 자체로 측정할 수 없다.
- gratuitous ARP와 switch 학습은 이 캡처 범위 밖이다.
