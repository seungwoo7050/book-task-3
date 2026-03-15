# DNS Packet Analysis Blog

이 문서 묶음은 `dns` 랩을 "DNS가 어떻게 동작하는가"라는 넓은 질문보다 "이 저장소가 준 두 trace만으로 어디까지 말할 수 있는가"라는 더 엄격한 질문으로 다시 읽는다. 현재 공개 답안은 `dns-nslookup.pcapng` 4패킷, `dns-web-browsing.pcapng` 2패킷만 사용해 A, MX, CNAME, authoritative flag, TTL을 해석하고, 보이지 않는 delegation chain이나 follow-up TCP는 추정하지 않는다. 따라서 이 lab의 핵심은 DNS 일반론보다 trace-based boundary를 지키는 분석 습관에 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/03-Packet-Analysis-Top-Down/dns/problem/README.md`
- 답안 경계: `README.md`, `analysis/README.md`, `analysis/src/dns-analysis.md`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/03-Packet-Analysis-Top-Down/dns/problem test`
- 보조 필터: `make -C .../dns/problem filter-queries`, `filter-responses`, `filter-browsing`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/03-Packet-Analysis-Top-Down/dns/problem test`
- 결과: `PASS: dns answer file passed content verification`
- 보조 필터에서 재확인한 값:
  - `example.com` 질의 대상: `8.8.8.8`
  - `www.ietf.org` 질의 대상: `1.1.1.1`
  - `example.com A -> 93.184.216.34 TTL 300`

## 지금 남기는 한계

- `dns-web-browsing.pcapng`는 2패킷뿐이라 후속 TCP 연결이나 TTL 감소를 직접 볼 수 없다.
- MX 응답은 `Type: MX`까지는 보이지만 answer detail은 malformed 처리로 끝까지 해석되지 않는다.
- authoritative nameserver의 IP는 trace에 들어 있지 않다.
