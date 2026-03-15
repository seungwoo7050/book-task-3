# DNS Packet Analysis 시리즈 맵

이 lab의 중심 질문은 "DNS를 많이 아는가"가 아니라 "주어진 trace가 허락하는 사실만으로 이름 해석 과정을 어디까지 재구성할 수 있는가"다. 현재 답안은 `example.com`의 A/MX 질의와 `www.ietf.org`의 A 질의만을 근거로, query/response 구조와 authoritative/non-authoritative 차이, TTL, CNAME을 읽어 낸다. 대신 delegation chain, repeated cache hit, follow-up TCP SYN 같은 항목은 `Not observable`로 남긴다.

## 이 lab를 읽는 질문

- 같은 DNS라 해도 A query, MX query, CNAME answer가 trace에서 어떻게 다르게 보이는가
- `Authoritative: 1`과 `Authoritative: 0`은 답변의 신뢰 원천을 어떻게 구분하는가
- Wireshark가 malformed나 extraneous data로 멈추면 어디서 해석을 멈춰야 하는가

## 이번에 사용한 근거

- `problem/README.md`
- `analysis/src/dns-analysis.md`
- `problem/Makefile`
- `problem/script/verify_answers.sh`
- 2026-03-14 재실행한 `filter-queries`, `filter-responses`, `filter-browsing`

## 이번 재실행에서 고정한 사실

- `dns-nslookup.pcapng` query 두 개는 모두 `8.8.8.8:53`으로 향한다.
- frame `#2`는 `example.com A 93.184.216.34 TTL 300`을 보여 준다.
- frame `#4`는 MX response이지만 `Type: MX`와 `TTL 300`만 확정되고 세부 MX host/preference는 malformed 처리로 끊긴다.
- `dns-web-browsing.pcapng`는 `www.ietf.org`에 대한 A query 1개와 response 1개만 포함하며, response는 CNAME answer 하나만 정식 decode된다.
