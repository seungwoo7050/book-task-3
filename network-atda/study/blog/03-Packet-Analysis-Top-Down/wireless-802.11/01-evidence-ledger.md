# 802.11 Wireless Packet Analysis Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/03-Packet-Analysis-Top-Down/wireless-802.11/problem/README.md`
- 답안 엔트리: `study/03-Packet-Analysis-Top-Down/wireless-802.11/analysis/src/wireless-analysis.md`
- 검증 스크립트: `study/03-Packet-Analysis-Top-Down/wireless-802.11/problem/script/verify_answers.sh`
- 실행 표면: `study/03-Packet-Analysis-Top-Down/wireless-802.11/problem/Makefile`

## 핵심 근거

- `beacons` 출력:
  - frame `1` AP `00:16:b6:f7:1d:51`, SSID hex for `30 Munroe St`, interval `100`
  - frame `2` AP `00:16:b6:f7:1d:52`, SSID hex for `linksys12`, interval `100`
- `probes` 출력:
  - frame `3` probe request from station `00:12:f0:1c:3e:82`
  - frame `4` probe response from AP `00:16:b6:f7:1d:51`
- `auth` and `assoc` outputs:
  - auth frames `5/6` algorithm `0`, success
  - assoc response frame `8` status `0x0000`, AID `0x0001`
- `data` and `ack` outputs:
  - frame `9` data with `To DS=True`, `From DS=False`
  - frame `10` ACK to station `00:12:f0:1c:3e:82`
- `frames-summary` shows 10-frame trace dominated by management subtypes and one data + one ACK.

## 테스트 근거

`make -C network-atda/study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`

결과:

- `PASS: wireless-802.11 answer file passed content verification`

## 이번에 고정한 해석

- 이 lab의 핵심은 data frame보다 그 전에 쌓이는 management ladder다.
- synthetic trace라 802.11 tagged parameter richness는 적지만, join sequence 자체는 오히려 또렷하게 보인다.
- Ethernet과 달리 discovery와 join을 위한 explicit frame family가 있다는 점이 가장 중요한 차이로 남는다.
