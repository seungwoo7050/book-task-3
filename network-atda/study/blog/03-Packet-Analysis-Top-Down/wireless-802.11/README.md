# 802.11 Wireless Packet Analysis Blog

이 문서 묶음은 `wireless-802.11` 랩을 "Wi-Fi frame 종류 소개"보다 "10-frame synthetic monitor trace만으로 station join 과정을 어디까지 복원할 수 있는가"라는 질문으로 다시 읽는다. 현재 공개 답안은 beacon 두 개, probe request/response, auth request/response, association request/response, data, ACK까지를 한 줄로 이어 붙인다. 따라서 이 lab의 핵심은 무선 LAN 전체를 설명하는 데 있지 않고, 802.11이 Ethernet과 달리 management frame을 앞세워 연결을 만드는 과정을 정확히 읽는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/03-Packet-Analysis-Top-Down/wireless-802.11/problem/README.md`
- 답안 경계: `README.md`, `analysis/README.md`, `analysis/src/wireless-analysis.md`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`
- 보조 필터: `make -C .../wireless-802.11/problem beacons`, `probes`, `auth`, `assoc`, `data`, `ack`, `frames-summary`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test`
- 결과: `PASS: wireless-802.11 answer file passed content verification`
- 보조 필터에서 재확인한 값:
  - beacons: SSIDs `30 Munroe St`, `linksys12`
  - auth frames `5/6`: Open System, success
  - assoc response frame `8`: status success, AID `0x0001`
  - data frame `9`, ACK frame `10`

## 지금 남기는 한계

- trace가 10 frame뿐인 compact synthetic capture라 retry, rate adaptation, real RF noise는 거의 보이지 않는다.
- WPA/EAPOL handshake 심화는 이 자료에 없다.
- probe/beacon tag detail도 실제 monitor capture보다 훨씬 단순화돼 있다.
