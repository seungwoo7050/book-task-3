# 802.11 Wireless Packet Analysis 문제 안내

## 이 문서의 역할

이 문서는 `802.11 Wireless Packet Analysis`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 답안을 먼저 보기보다 trace 범위와 질문을 먼저 이해하는 데 초점을 둡니다.

## 문제 목표

미리 캡처된 802.11 무선 trace를 분석해 beacon, probe, authentication, association, data frame이 어떻게 오가며 무선 LAN 연결이 성립하는지 이해합니다.

## 제공 trace

| 파일 | 시나리오 | 설명 |
| :--- | :--- | :--- |
| `wireless-trace.pcap` | 무선 trace | beacon, probe request/response, association, 데이터 전송이 담긴 monitor mode 캡처 |

## 풀어야 할 질문

### 파트 1. Beacon frame

1. trace에서 가장 많은 beacon을 보내는 AP들의 SSID는 무엇입니까?
2. 한 AP가 successive beacon frame을 보내는 시간 간격은 어느 정도입니까?
3. 특정 AP beacon frame의 source MAC 주소는 무엇이며, 이것이 BSSID와 같은 값입니까?
4. beacon frame이 광고하는 supported rates와 extended supported rates는 무엇입니까?
5. beacon frame의 capability information은 무엇이며, WEP/WPA/WPA2 같은 보안 정보 요소를 확인할 수 있습니까?

### 파트 2. Probe request / response

1. probe request frame의 source MAC 주소와 SSID는 무엇입니까?
2. 대응하는 probe response frame의 source MAC 주소는 무엇이며, beacon에서 본 AP와 같은 장치입니까?
3. probe response의 information elements는 같은 AP의 beacon frame과 동일합니까? 차이가 있다면 무엇입니까?
4. probe request frame의 destination MAC 주소는 무엇이며, 왜 그 주소가 사용됩니까?

### 파트 3. Authentication과 Association

1. Authentication frame에서 사용된 authentication algorithm은 무엇입니까(Open System 또는 Shared Key)?
2. Authentication request/response의 source/destination MAC 주소와 status code는 무엇입니까?
3. Association Request frame에서 station은 AP에 어떤 정보를 전달합니까?
4. Association Response의 status code는 무엇이며, station에 어떤 AID가 할당됩니까?
5. 초기 probe부터 association 성공까지의 management frame 순서를 frame 번호와 함께 정리해 보세요.

### 파트 4. Data frame과 frame 구조

1. 802.11 data frame header에는 몇 개의 MAC address field가 있으며, `To DS`/`From DS` 비트에 따라 어떤 역할을 합니까?
2. data frame, beacon frame, ACK frame의 Frame Control Type/Subtype 값은 각각 무엇입니까?
3. data frame의 `Duration/ID` field 값은 무엇이며 무엇을 의미합니까?
4. 802.11 ACK control frame을 찾아 보세요. 이 frame에는 주소 field가 몇 개 있으며, 바로 앞선 data frame과 어떤 관계를 가집니까?

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 정확성 | 정확한 packet/frame 번호와 field 값을 사용합니다. |
| 완결성 | 모든 질문에 근거를 포함해 답합니다. |
| 이해도 | 프로토콜 메커니즘을 이해한 설명을 제시합니다. |
| 근거성 | Wireshark field와 trace evidence를 직접 인용합니다. |
