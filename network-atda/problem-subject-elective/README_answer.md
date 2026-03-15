# network-atda 비필수 답안지

이 문서는 network-atda 확장 과제를 code형과 packet-analysis형으로 나눠 요약한 답안지다. 코드형은 실제 구현 파일과 테스트를, packet-analysis형은 trace와 Makefile target을 핵심 근거로 둔다.

## Application Protocols & Sockets

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [dns](dns_answer.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/dns/problem test` |
| [ethernet-arp](ethernet-arp_answer.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test` |
| [http](http_answer.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/http/problem test` |
| [http2-quic](http2-quic_answer.md) | 시작 위치의 구현을 완성해 총 12개 질문에 모두 답한다, frame 번호, stream ID, packet type, connection ID 같은 근거를 직접 적는다, HTTP/2와 QUIC의 차이를 단순 "더 빠르다"가 아니라 구조 차이로 설명한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/http2-quic/problem test` |
| [icmp-pinger](icmp-pinger_answer.md) | 시작 위치의 구현을 완성해 패킷 생성: ICMP Echo Request 형식이 올바릅니다, 체크섬: 인터넷 체크섬이 정확합니다, 응답 파싱: Echo Reply를 올바르게 추출하고 검증합니다를 한 흐름으로 설명하고 검증한다. 핵심은 internet_checksum와 build_echo_request, parse_echo_reply 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test` |
| [ip-icmp](ip-icmp_answer.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/ip-icmp/problem test` |
| [routing](routing_answer.md) | 시작 위치의 구현을 완성해 Bellman-Ford 적용: DV update 식을 올바르게 구현합니다, 수렴: 최단 경로로 수렴합니다, 분산성: 각 노드가 지역 정보만으로 계산합니다를 한 흐름으로 설명하고 검증한다. 핵심은 load_topology와 DVNode, simulate 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/04-Network-Diagnostics-and-Routing/routing/problem test` |
| [selective-repeat](selective-repeat_answer.md) | 시작 위치의 구현을 완성해 선택 재전송: timeout이 난 패킷만 다시 전송합니다, 수신 버퍼링: out-of-order 패킷을 버퍼링하고 순서대로 전달합니다, ACK 처리: 개별 ACK로 sender 상태를 정확히 갱신합니다를 한 흐름으로 설명하고 검증한다. 핵심은 selective_repeat_send_receive와 load_messages, main 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/selective-repeat/problem test` |
| [smtp-client](smtp-client_answer.md) | 시작 위치의 구현을 완성해 완전한 SMTP 대화: 필수 SMTP 명령을 올바른 순서로 전송합니다, 응답 코드 검증: 각 단계에서 응답 코드를 확인하고 다음 단계로 진행합니다, 메시지 전송: 메일 본문이 정상적으로 전달되거나 로컬 디버그 서버에 기록됩니다를 한 흐름으로 설명하고 검증한다. 핵심은 recv_reply와 send_command, check_reply 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/smtp-client/problem test` |
| [tcp-udp](tcp-udp_answer.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/tcp-udp/problem test` |
| [tls-ssl](tls-ssl_answer.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/tls-ssl/problem test` |
| [traceroute](traceroute_answer.md) | 시작 위치의 구현을 완성해 TTL 처리: TTL 증가에 따라 hop을 순서대로 드러냅니다, ICMP 파싱: Time Exceeded와 Port Unreachable을 구분합니다, Probe 매칭: 응답과 probe를 정확히 연결합니다를 한 흐름으로 설명하고 검증한다. 핵심은 ProbeObservation와 build_probe_port, parse_icmp_response 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/04-Network-Diagnostics-and-Routing/traceroute/problem test` |
| [udp-pinger](udp-pinger_answer.md) | 시작 위치의 구현을 완성해 정확한 메시지 전송: 10개의 UDP ping 메시지를 형식에 맞게 전송합니다, RTT 계산: 응답이 온 ping마다 RTT를 올바르게 계산합니다, Timeout 처리: 1초 안에 응답이 없으면 손실로 판정합니다를 한 흐름으로 설명하고 검증한다. 핵심은 main 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/udp-pinger/problem test` |
| [web-proxy](web-proxy_answer.md) | 시작 위치의 구현을 완성해 요청 전달: 프록시가 원 서버로 요청을 정확히 전달합니다, 응답 중계: 클라이언트가 원 서버 응답을 완전하게 받습니다, 캐시 재사용: 반복 요청을 캐시에서 처리합니다를 한 흐름으로 설명하고 검증한다. 핵심은 parse_url와 get_cache_path, fetch_from_origin 흐름을 구현하고 테스트를 통과시키는 것이다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/web-proxy/problem test` |
| [wireless-80211](wireless-80211_answer.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
