# 802.11 Wireless Packet Analysis 개발 타임라인

현재 답안을 다시 읽으면 이 lab의 흐름은 802.11 field glossary를 늘어놓는 방식이 아니다. 오히려 station이 AP를 발견하고, 확인하고, 인증하고, 연관한 뒤 처음 data를 보내는 10-frame ladder를 한 단계씩 복원하는 구조에 가깝다. 전환점은 다섯 번이다.

## 1. beacon 두 개가 먼저 주변 wireless world를 연다

frames `1`과 `2`는 각각 `30 Munroe St`, `linksys12`를 광고하는 beacon이다. beacon interval은 둘 다 `100 TU`다. 이 첫 장면 때문에 wireless는 Ethernet처럼 이미 선이 꽂혀 있는 상태가 아니라, 먼저 주변 BSS를 discover해야 하는 환경으로 보이기 시작한다.

즉 beacon은 data plane 이전에 존재하는 "네트워크 존재 신호"다.

## 2. station은 probe request/response로 목표 AP를 좁힌다

frame `3`에서 station `00:12:f0:1c:3e:82`는 broadcast probe request를 뿌리고, frame `4`에서 AP `00:16:b6:f7:1d:51`이 probe response로 답한다. 답안이 이 구간을 beacon과 따로 적는 이유는, passive discovery와 active querying이 구분되기 때문이다.

그래서 이 단계는 "SSID를 본다"가 아니라, station이 특정 SSID를 적극적으로 찾는 장면으로 읽혀야 한다.

## 3. authentication과 association은 둘 다 success여도 서로 다른 문턱이다

frames `5/6`은 Open System auth request/response다. 이어 frames `7/8`은 association request/response다. 둘 다 success status를 주지만 의미는 다르다. auth는 "이 방식으로 대화할 수 있느냐"에 가깝고, association은 "이 BSS의 정식 member로 state를 할당받았느냐"에 가깝다. frame `8`의 AID `0x0001`이 바로 그 할당 흔적이다.

이 분리가 802.11을 wired Ethernet과 가장 다르게 느끼게 만드는 부분이다.

## 4. 첫 data frame에서야 비로소 station-ap forwarding 관계가 보인다

frame `9`는 `To DS=True`, `From DS=False`인 data frame이다. 이제야 management가 아니라 실제 payload-bearing traffic이 보인다. station MAC, AP BSSID, DS direction bit가 함께 나타나므로, 802.11 주소 필드가 단순 src/dst만은 아니라는 점도 드러난다.

즉 이 lab는 data frame이 나오기 전까지의 긴 준비 과정을 보여 주면서, wireless data delivery가 join state 위에 얹혀 있다는 사실을 강조한다.

## 5. ACK frame이 마지막으로 link-layer reliability의 최소 흔적을 남긴다

frame `10`은 ACK frame이고 receiver address는 station `00:12:f0:1c:3e:82`다. data frame 하나 뒤에 ACK 하나가 붙으면서, 무선 링크 계층이 여전히 per-frame acknowledgment를 중요하게 다룬다는 최소한의 흔적이 남는다.

결국 이 lab의 마지막 전환점은 management-heavy join ladder에서, 아주 짧은 data + ACK exchange로 넘어가는 순간이다. 작지만 802.11의 성격을 압축적으로 보여 주는 trace다.

## 지금 남는 한계

현재 자료는 real monitor-mode capture보다 훨씬 단순하다. WPA handshake, retries, rate adaptation, noisy RF environment는 거의 보이지 않는다. 그래도 beacon부터 ACK까지의 join ladder만큼은 교재보다 오히려 더 압축적으로 읽힌다.
