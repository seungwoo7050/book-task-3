# TLS Packet Analysis 문제 안내

## 이 문서의 역할

이 문서는 `TLS Packet Analysis`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 답안을 먼저 보기보다 trace 범위와 질문을 먼저 이해하는 데 초점을 둡니다.

## 문제 목표

미리 캡처된 HTTPS/TLS trace를 분석해, ClientHello부터 암호화된 Application Data까지의 흐름과 TLS 버전 차이를 이해합니다.

## 제공 trace

| 파일 | 시나리오 | 설명 |
| :--- | :--- | :--- |
| `tls-trace.pcap` | TLS trace | 전체 TLS handshake, certificate 교환, 암호화된 application data가 포함된 캡처 |

## 풀어야 할 질문

### 파트 1. ClientHello (Q1-Q5)

1. ClientHello 메시지의 TLS record content type은 무엇입니까? record layer와 handshake layer가 가리키는 TLS version은 어떻게 다릅니까?
2. ClientHello가 광고하는 cipher suite는 무엇입니까? 개수와 함께 최소 3개 이상 이름을 적어 보세요.
3. ClientHello에 SNI(Server Name Indication) extension이 있습니까? 있다면 어떤 서버 이름이 들어 있습니까?
4. 클라이언트가 지원한다고 알리는 TLS version은 무엇입니까? `supported_versions` extension이나 handshake version field를 확인해 보세요.
5. ClientHello에 포함된 다른 notable extension을 최소 3개 찾아 목적을 간단히 설명해 보세요.

### 파트 2. ServerHello와 Certificate (Q6-Q11)

1. ServerHello에서 서버가 선택한 cipher suite는 무엇입니까? 그 이름의 각 구성 요소는 무엇을 뜻합니까?
2. 최종 협상된 TLS version은 무엇이며, 어디에서 확인할 수 있습니까?
3. Certificate 메시지에는 인증서가 몇 개 들어 있으며, 각 인증서의 subject(Common Name)는 무엇입니까?
4. 서버(leaf) 인증서의 issuer는 누구입니까? root CA 인증서도 서버가 보내는 체인에 포함되어 있습니까?
5. 서버 인증서의 유효 기간(Not Before / Not After)과 서명 알고리즘은 무엇입니까?
6. ServerHello 또는 이어지는 메시지에 ServerKeyExchange가 포함되어 있습니까? 있다면 어떤 key exchange parameter가 들어 있습니까?

### 파트 3. Handshake 완료 (Q12-Q16)

1. ChangeCipherSpec 메시지는 몇 개이며 누가 보냅니까?
2. ChangeCipherSpec 다음에 오는 메시지는 무엇입니까? 내용을 읽을 수 있습니까? 왜 그렇습니까?
3. trace에 나타나는 TLS handshake 메시지 전체 순서를 frame 번호와 송신자(client/server)와 함께 적어 보세요.
4. 첫 ClientHello부터 첫 Application Data record까지 TLS handshake에 몇 번의 round trip이 필요합니까?
5. 이 세션이 TLS 1.3이라면 TLS 1.2와 비교했을 때 어떤 차이가 보입니까? 메시지 흐름을 근거로 설명해 보세요.

### 파트 4. Application Data와 Record Protocol (Q17-Q20)

1. Application Data record를 하나 찾아 TLS record content type 값과 암호화 payload 길이를 적어 보세요.
2. 복호화 없이도 안에 실린 애플리케이션 프로토콜(예: HTTP)을 추정할 수 있습니까? handshake 중 plaintext로 드러나는 정보가 있다면 무엇입니까?
3. 여러 Application Data record의 길이는 일정합니까, 가변적입니까? 가장 큰 TLS record 크기는 얼마입니까?
4. `SSLKEYLOGFILE` 같은 pre-master secret 로그가 있다면 Wireshark에서 세션을 복호화해 어떤 HTTP 요청/응답이 보이는지 확인해 보세요.

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| 정확성 | 정확한 packet/frame 번호와 field 값을 사용합니다. |
| 완결성 | 모든 질문에 근거를 포함해 답합니다. |
| 이해도 | 프로토콜 메커니즘을 이해한 설명을 제시합니다. |
| 근거성 | Wireshark field와 trace evidence를 직접 인용합니다. |
