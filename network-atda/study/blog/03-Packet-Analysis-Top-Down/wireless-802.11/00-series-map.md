# 802.11 Wireless Packet Analysis 시리즈 맵

이 lab의 중심 질문은 "wireless LAN에서 연결이 실제로 어떤 management 단계들을 거쳐 성립하는가"다. 현재 trace는 `30 Munroe St`와 `linksys12` beacon으로 시작해, station `00:12:f0:1c:3e:82`가 probe, auth, association을 거쳐 data frame을 보내고 AP ACK를 받는 장면까지 압축해서 보여 준다.

## 이 lab를 읽는 질문

- beacon과 probe는 어떤 차이로 네트워크 discovery를 나누는가
- authentication과 association은 둘 다 성공 status를 주지만 역할이 왜 다른가
- `To DS`/`From DS`와 ACK frame을 보면 station-ap data exchange 구조가 어떻게 보이는가

## 이번에 사용한 근거

- `problem/README.md`
- `analysis/src/wireless-analysis.md`
- `problem/Makefile`
- `problem/script/verify_answers.sh`
- 2026-03-14 재실행한 `beacons`, `probes`, `auth`, `assoc`, `data`, `ack`, `frames-summary`

## 이번 재실행에서 고정한 사실

- beacon frames `1/2`의 SSID는 `30 Munroe St`, `linksys12`이고 beacon interval은 둘 다 `100`.
- probe request frame `3`은 broadcast, probe response frame `4`는 AP unicast다.
- auth request/response frames `5/6`은 algorithm `0`, status success다.
- association response frame `8`은 success와 AID `0x0001`을 담고, data frame `9` 뒤 ACK frame `10`이 따라온다.
