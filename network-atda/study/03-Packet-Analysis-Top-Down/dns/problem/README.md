# DNS Packet Analysis 문제 안내

## 이 문서의 역할

이 문서는 `DNS Packet Analysis`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 답안을 먼저 보기보다 trace 범위와 질문을 먼저 이해하는 데 초점을 둡니다.

## 문제 목표

미리 캡처된 DNS trace를 Wireshark로 분석해, 도메인 이름이 IP 주소로 해석되는 과정과 record type, 캐시 TTL의 의미를 이해합니다.

## 제공 trace

| 파일 | 시나리오 | 설명 |
| :--- | :--- | :--- |
| `dns-nslookup.pcapng` | `nslookup` 질의 | `nslookup`으로 생성한 DNS query/response를 담은 trace |
| `dns-web-browsing.pcapng` | 웹 브라우징 | 웹 페이지를 열 때 발생한 DNS 질의 trace |

## 풀어야 할 질문

### 파트 1. `nslookup` trace

1. DNS는 어떤 전송 계층 프로토콜을 사용합니까? DNS 서버는 어떤 포트 번호를 사용합니까?
2. DNS query 메시지는 어떤 IP 주소로 보내졌습니까? 이것이 기본 로컬 DNS 서버 주소인지 어떻게 확인할 수 있습니까?
3. DNS query의 type은 무엇입니까? query 안에 answer가 포함되어 있습니까?
4. DNS response에는 answer가 몇 개 들어 있으며, 각 answer는 무엇을 담고 있습니까?
5. 질의한 호스트에 대해 `CNAME`이 있다면 무엇이며, 어떤 IP 주소들이 반환됩니까?
6. 메일 서버(MX record) 질의에 대한 응답에서는 어떤 서버 이름과 preference 값이 반환됩니까?

### 파트 2. Authoritative / Non-Authoritative 응답

1. DNS query 메시지는 어떤 IP 주소로 보내졌으며, 이것이 기본 로컬 DNS 서버 주소입니까?
2. 질의 타입은 무엇이며, query 메시지에 answer가 들어 있습니까?
3. response 메시지에서 authoritative nameserver를 찾아 보세요. authoritative answer와 non-authoritative answer의 차이는 무엇입니까?
4. response에 authoritative nameserver의 IP 주소도 포함되어 있습니까? 있다면 무엇입니까?

### 파트 3. 웹 브라우징 중 DNS (`dns-web-browsing.pcapng`)

1. `www.ietf.org`를 열 때 발생한 첫 DNS query는 어느 IP 주소로 향합니까? 이것이 로컬 DNS resolver 주소입니까?
2. 해당 DNS query의 type은 무엇이며, query 안에 answer가 있습니까?
3. DNS response에는 answer가 몇 개 들어 있습니까? 각 answer의 type, 값, TTL을 적어 보세요.
4. 이어지는 TCP SYN 패킷의 목적지 IP 주소는 DNS response에 있던 주소들 중 하나와 일치합니까?
5. 시간이 지난 뒤 발생한 DNS query에서 캐시된 record의 TTL이 달라졌습니까? 이것이 DNS 캐시에 대해 무엇을 말해 줍니까?
6. 하나의 페이지 로드에서 총 몇 개의 DNS query/response가 발생했습니까? 어떤 record type(A, AAAA, CNAME 등)이 질의되었습니까?

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 정확성 | 정확한 packet/frame 번호와 field 값을 사용합니다. |
| 완결성 | 모든 질문에 근거를 포함해 답합니다. |
| 이해도 | 프로토콜 메커니즘을 이해한 설명을 제시합니다. |
| 근거성 | Wireshark field와 trace evidence를 직접 인용합니다. |
