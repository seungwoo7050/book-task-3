# DNS Packet Analysis 시리즈 지도

## 이 프로젝트를 한 줄로

DNS를 "도메인 이름을 IP로 바꿔 준다"에서 멈추지 않고, query/response 쌍과 trace의 관찰 한계를 함께 적어 내려간 기록이다.

## 시작 전에 고정한 자료

- 제공 trace: `problem/data/dns-nslookup.pcapng`, `dns-web-browsing.pcapng`
- 실행 진입점: `problem/Makefile`
- 사용자 답안: `study/03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`
- 보조 개념 문서: `docs/concepts/wireshark-dns.md`

## 이 시리즈에서 따라갈 질문

1. DNS query와 response를 최소 몇 개의 필드로 묶어야 "이 요청의 답이 이것"이라고 말할 수 있는가.
2. `8.8.8.8` 같은 resolver 주소를 trace만으로 어디까지 해석할 수 있고, 어디부터는 추정이 되는가.
3. authoritative bit, TTL, answer count는 어떤 frame에서 바로 확인되는가.
4. malformed response나 packet 수가 너무 작은 trace에서는 어떤 답을 과감하게 `관찰 불가`로 남겨야 하는가.

## 검증 명령

- query 확인: `make -C study/03-Packet-Analysis-Top-Down/dns/problem filter-queries`
- response 확인: `make -C study/03-Packet-Analysis-Top-Down/dns/problem filter-responses`
- browsing trace: `make -C study/03-Packet-Analysis-Top-Down/dns/problem filter-browsing`
- 답안 검증: `make -C study/03-Packet-Analysis-Top-Down/dns/problem test`

## 글 구성

| 파일 | 역할 |
| :--- | :--- |
| `00-series-map.md` | query/response 구조와 관찰 한계를 먼저 선언한다. |
| `10-development-timeline.md` | nslookup trace를 먼저 읽고, 그다음 browsing trace로 "관찰 가능한 범위"를 다시 줄여 본다. |
