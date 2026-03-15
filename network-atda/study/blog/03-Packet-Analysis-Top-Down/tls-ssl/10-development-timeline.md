# TLS Packet Analysis 개발 타임라인

현재 답안을 다시 읽으면 이 lab의 흐름은 TLS message catalog를 다 적는 식이 아니다. 오히려 "plain negotiation이 얼마나 보이다가, 어느 순간부터 payload visibility가 끊기는가"를 6-frame synthetic trace 안에서 순서대로 확인하는 방식에 가깝다. 전환점은 네 번이다.

## 1. 먼저 TCP 3-way handshake 뒤에 TLS handshake가 올라탄다는 기본 틀을 세운다

trace의 frames `1/2/3`은 TCP connection establishment다. 그 뒤 frame `4`부터 비로소 TLS record가 나온다. 이 순서 자체가 중요한 이유는, TLS가 transport 위에 올라간 secure session layer라는 점을 trace가 그대로 보여 주기 때문이다.

즉 첫 단계는 TLS를 독립 프로토콜처럼 보는 대신, TCP 위에 추가된 negotiation layer로 위치시키는 것이다.

## 2. ClientHello에서는 아직 협상 정보가 꽤 많이 노출된다

frame `4`의 ClientHello는 `0x0303`, cipher suites `0x1301,0x1302`, empty SNI를 보여 준다. answer markdown는 이 단계에서 cipher suite 목록과 version field를 읽는다. 아직 encryption이 시작되지 않았기 때문에 "무엇을 제안했는가"는 그대로 보인다.

이 장면 덕분에 TLS trace는 무조건 opaque하다는 오해를 피하게 된다. 초기 handshake는 오히려 많은 협상 메타데이터를 노출한다.

## 3. ServerHello와 Certificate에서 협상 결과는 보이지만 identity detail은 trace와 도구 양쪽에서 흐려진다

frame `5`는 selected suite `0x1301`을 보여 주고 certificate handshake도 포함한다. 그러나 현재 trace는 certificate를 malformed로 표시하고, 현재 환경의 `make certs`도 `docs/concepts/wireshark-tls.md`가 예시로 드는 `x509sat.utf8String` field를 지원하지 않아 실패했다. 따라서 "certificate가 있다"는 사실과 "무엇이 선택됐다"는 사실까지는 말할 수 있지만, issuer/subject chain detail을 끝까지 안정적으로 읽을 수는 없다.

이 지점이 이 lab의 핵심 절제 포인트다. TLS를 다 읽고 싶은 마음과, 현재 trace/도구가 허락하는 범위를 분리해야 문서 품질이 유지된다.

## 4. ChangeCipherSpec 이후에는 application 의미가 아니라 opaque length만 남는다

frame `6`에서는 `ChangeCipherSpec` 뒤 `Application Data`가 보인다. record length는 보이지만 plaintext HTTP message는 더 이상 직접 보이지 않는다. answer markdown가 "context상 HTTP일 수 있다"와 "plaintext를 본 것은 아니다"를 구분하는 이유가 바로 여기 있다.

결국 이 lab의 마지막 전환점은 handshake visibility에서 encrypted payload opacity로 넘어가는 순간을 확인하는 것이다. TLS의 목적이 trace에서 바로 체감되는 구간이기도 하다.

## 지금 남는 한계

현재 trace는 synthetic하고 짧다. full TLS 1.2/1.3 canonical message set, rich extensions, certificate details, decrypted application layer는 제공하지 않는다. 그래도 negotiation이 어디까지 보이고, 그 뒤 무엇이 사라지는지라는 핵심 교훈은 충분히 선명하다.
