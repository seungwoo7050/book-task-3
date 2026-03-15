# Ethernet and ARP Packet Analysis Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/03-Packet-Analysis-Top-Down/ethernet-arp/problem/README.md`
- 답안 엔트리: `study/03-Packet-Analysis-Top-Down/ethernet-arp/analysis/src/ethernet-arp-analysis.md`
- 검증 스크립트: `study/03-Packet-Analysis-Top-Down/ethernet-arp/problem/script/verify_answers.sh`
- 실행 표면: `study/03-Packet-Analysis-Top-Down/ethernet-arp/problem/Makefile`

## 핵심 근거

- `filter-arp` 출력:
  - frame `1` `00:11:22:33:44:55 -> ff:ff:ff:ff:ff:ff`, opcode `1`, sender IP `192.168.0.2`, target IP `192.168.0.1`
  - frame `2` `66:77:88:99:aa:bb -> 00:11:22:33:44:55`, opcode `2`, sender IP `192.168.0.1`
- `filter-ethernet` 출력:
  - frames `1/2` EtherType `0x0806`
  - frame `3` EtherType `0x0800`
- `filter-broadcast` 출력:
  - broadcast frame은 frame `1` 하나뿐이다.

## 테스트 근거

`make -C network-atda/study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test`

결과:

- `PASS: ethernet-arp answer file passed content verification`

## 이번에 고정한 해석

- 이 trace는 ARP cache miss 직후의 가장 압축된 장면이다.
- reply가 frame `1`의 sender MAC을 destination으로 그대로 되돌린다는 사실이, ARP가 broadcast discovery 뒤 unicast answer로 수렴함을 보여 준다.
- frame `3`까지 확인해야만 "ARP reply가 실제 다음 IPv4 frame에 반영됐다"는 문장을 쓸 수 있다.
