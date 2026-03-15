# DNS Packet Analysis Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/03-Packet-Analysis-Top-Down/dns/problem/README.md`
- 답안 엔트리: `study/03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`
- 검증 스크립트: `study/03-Packet-Analysis-Top-Down/dns/problem/script/verify_answers.sh`
- 실행 표면: `study/03-Packet-Analysis-Top-Down/dns/problem/Makefile`

## 핵심 근거

- `dns-analysis.md`는 trace limitation을 먼저 선언하고, 보이지 않는 항목은 추정하지 않는다는 기준을 고정한다.
- `filter-queries` 출력:
  - frame `1` `8.8.8.8 example.com type 1`
  - frame `3` `8.8.8.8 example.com type 15`
- `filter-responses` 출력:
  - frame `2` `example.com type 1 -> 93.184.216.34 TTL 300`
  - frame `4` `example.com type 15 TTL 300`
- `filter-browsing` 출력:
  - frame `1` query `www.ietf.org`
  - frame `2` response `www.ietf.org`

## 테스트 근거

`make -C network-atda/study/03-Packet-Analysis-Top-Down/dns/problem test`

결과:

- `PASS: dns answer file passed content verification`

## 이번에 고정한 해석

- 이 lab는 DNS resolver 동작 전체를 재현하는 랩이 아니라, 짧은 trace에서 query/response 구조를 읽는 랩이다.
- authoritative vs non-authoritative 차이는 flag로 확인할 수 있지만, authoritative NS IP나 delegation chain은 trace가 없으므로 답을 만들어 내면 안 된다.
- web trace는 `CNAME` decode까지만 확실하며, 이후 TCP SYN이나 TTL 감소 해석은 현재 증거로는 불가능하다.
