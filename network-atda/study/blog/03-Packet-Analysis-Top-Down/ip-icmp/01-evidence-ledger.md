# IP and ICMP Packet Analysis Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/03-Packet-Analysis-Top-Down/ip-icmp/problem/README.md`
- 답안 엔트리: `study/03-Packet-Analysis-Top-Down/ip-icmp/analysis/src/ip-icmp-analysis.md`
- 검증 스크립트: `study/03-Packet-Analysis-Top-Down/ip-icmp/problem/script/verify_answers.sh`
- 실행 표면: `study/03-Packet-Analysis-Top-Down/ip-icmp/problem/Makefile`

## 핵심 근거

- `filter-icmp` 출력:
  - frame `1` Echo Request `ttl=1 type/code=8/0 id=0x0fa0`
  - frame `2` router reply includes `10.0.0.1` outer source and embedded original probe
  - frame `4` second router `172.16.0.1 type/code=11/0`
  - frame `6` destination reply `type/code=0/0`
- `filter-fragments` 출력:
  - frame `1` `id=0x3039 mf=True offset=0 len=1420`
  - frame `2` `id=0x3039 mf=True offset=175 len=1420`
  - frame `3` `id=0x3039 mf=False offset=350 len=728`
- `ip-icmp-analysis.md`는 reassembly가 destination host에서 일어난다는 점과 `trace` payload 5 bytes까지 계산한다.

## 테스트 근거

`make -C network-atda/study/03-Packet-Analysis-Top-Down/ip-icmp/problem test`

결과:

- `PASS: ip-icmp answer file passed content verification`

## 이번에 고정한 해석

- traceroute trace는 TTL이 줄어드는 장면보다 TTL을 의도적으로 늘려 가며 router ICMP를 끌어내는 장면으로 읽어야 한다.
- fragmentation trace의 핵심은 fragment count가 아니라, `offset*8`과 `ip.len`을 곱해 reassembly byte range를 다시 계산할 수 있다는 데 있다.
- ICMP는 "ping 프로토콜" 하나가 아니라, path discovery와 error reporting을 함께 맡는 control surface로 보인다.
