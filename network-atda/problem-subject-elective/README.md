# network-atda 비필수 문제지

여기서 `elective`는 중요하지 않다는 뜻이 아니라, 핵심 경로 다음에 읽는 확장 문제라는 뜻입니다. 응용 프로토콜, packet analysis, 진단 도구처럼 네트워크 감각을 넓혀 주는 항목을 모았습니다.

## Application Protocols & Sockets

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [dns](dns.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/dns/problem test` |
| [ethernet-arp](ethernet-arp.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test` |
| [http](http.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/http/problem test` |
| [http2-quic](http2-quic.md) | 시작 위치의 구현을 완성해 총 12개 질문에 모두 답한다, frame 번호, stream ID, packet type, connection ID 같은 근거를 직접 적는다, HTTP/2와 QUIC의 차이를 단순 "더 빠르다"가 아니라 구조 차이로 설명한다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/http2-quic/problem test` |
| [icmp-pinger](icmp-pinger.md) | 시작 위치의 구현을 완성해 패킷 생성: ICMP Echo Request 형식이 올바릅니다, 체크섬: 인터넷 체크섬이 정확합니다, 응답 파싱: Echo Reply를 올바르게 추출하고 검증합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test` |
| [ip-icmp](ip-icmp.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/ip-icmp/problem test` |
| [routing](routing.md) | 시작 위치의 구현을 완성해 Bellman-Ford 적용: DV update 식을 올바르게 구현합니다, 수렴: 최단 경로로 수렴합니다, 분산성: 각 노드가 지역 정보만으로 계산합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/04-Network-Diagnostics-and-Routing/routing/problem test` |
| [selective-repeat](selective-repeat.md) | 시작 위치의 구현을 완성해 선택 재전송: timeout이 난 패킷만 다시 전송합니다, 수신 버퍼링: out-of-order 패킷을 버퍼링하고 순서대로 전달합니다, ACK 처리: 개별 ACK로 sender 상태를 정확히 갱신합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/02-Reliable-Transport/selective-repeat/problem test` |
| [smtp-client](smtp-client.md) | 시작 위치의 구현을 완성해 완전한 SMTP 대화: 필수 SMTP 명령을 올바른 순서로 전송합니다, 응답 코드 검증: 각 단계에서 응답 코드를 확인하고 다음 단계로 진행합니다, 메시지 전송: 메일 본문이 정상적으로 전달되거나 로컬 디버그 서버에 기록됩니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/smtp-client/problem test` |
| [tcp-udp](tcp-udp.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/tcp-udp/problem test` |
| [tls-ssl](tls-ssl.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/tls-ssl/problem test` |
| [traceroute](traceroute.md) | 시작 위치의 구현을 완성해 TTL 처리: TTL 증가에 따라 hop을 순서대로 드러냅니다, ICMP 파싱: Time Exceeded와 Port Unreachable을 구분합니다, Probe 매칭: 응답과 probe를 정확히 연결합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/04-Network-Diagnostics-and-Routing/traceroute/problem test` |
| [udp-pinger](udp-pinger.md) | 시작 위치의 구현을 완성해 정확한 메시지 전송: 10개의 UDP ping 메시지를 형식에 맞게 전송합니다, RTT 계산: 응답이 온 ping마다 RTT를 올바르게 계산합니다, Timeout 처리: 1초 안에 응답이 없으면 손실로 판정합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/udp-pinger/problem test` |
| [web-proxy](web-proxy.md) | 시작 위치의 구현을 완성해 요청 전달: 프록시가 원 서버로 요청을 정확히 전달합니다, 응답 중계: 클라이언트가 원 서버 응답을 완전하게 받습니다, 캐시 재사용: 반복 요청을 캐시에서 처리합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/01-Application-Protocols-and-Sockets/web-proxy/problem test` |
| [wireless-80211](wireless-80211.md) | 시작 위치의 구현을 완성해 정확성: 정확한 packet/frame 번호와 field 값을 사용합니다, 완결성: 모든 질문에 근거를 포함해 답합니다, 이해도: 프로토콜 메커니즘을 이해한 설명을 제시합니다를 한 흐름으로 설명하고 검증한다. | `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
