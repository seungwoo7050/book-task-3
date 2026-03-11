# 03. Packet Analysis Top-Down

HTTP에서 TLS까지 내려가며 Wireshark trace를 문제-증거-해설 구조로 읽는 단계입니다.

## 프로젝트 카탈로그

| 프로젝트 | 문제 | 이 레포의 답 | 검증 | 상태 | 왜 이 단계에 있는가 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`HTTP Packet Analysis`](http/README.md) | `Computer Networking: A Top-Down Approach`의 HTTP Wireshark 랩을 현재 저장소의 `problem/analysis/docs` 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/http/problem test` | `verified` | 사람이 읽을 수 있는 텍스트 프로토콜인 HTTP를 시작점으로 삼아, Wireshark로 무엇을 관찰하고 어떤 근거로 설명해야 하는지 감을 잡기 좋습니다. |
| [`DNS Packet Analysis`](dns/README.md) | `Computer Networking: A Top-Down Approach`의 DNS Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/dns/problem test` | `verified` | HTTP 다음 단계에서 이름 해석 계층을 관찰하며, 패킷 분석이 응용 계층 내부 프로토콜에도 그대로 적용된다는 점을 보여 줍니다. |
| [`TCP and UDP Packet Analysis`](tcp-udp/README.md) | `Computer Networking: A Top-Down Approach`의 TCP/UDP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test` | `verified` | 응용 계층 랩 다음에 전송 계층의 상태와 오버헤드를 직접 관찰하면서, 이후 신뢰 전송 구현 트랙과 연결되는 근거를 쌓을 수 있습니다. |
| [`IP and ICMP Packet Analysis`](ip-icmp/README.md) | `Computer Networking: A Top-Down Approach`의 IP/ICMP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test` | `verified` | 전송 계층 랩 다음에 네트워크 계층 헤더와 제어 메시지를 직접 읽으며, 이후 `ICMP Pinger`와 `Traceroute` 구현 프로젝트와 맞물리게 합니다. |
| [`Ethernet and ARP Packet Analysis`](ethernet-arp/README.md) | `Computer Networking: A Top-Down Approach`의 Ethernet/ARP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test` | `verified` | 네트워크 계층 랩 다음에 링크 계층 주소 해석을 보며, 상위 계층 IP 주소와 하위 계층 MAC 주소가 어떻게 연결되는지 확인하게 합니다. |
| [`802.11 Wireless Packet Analysis`](wireless-802.11/README.md) | `Computer Networking: A Top-Down Approach`의 802.11 Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test` | `verified` | Ethernet/ARP 다음에 무선 링크 계층의 차이를 관찰하며, 같은 링크 계층이라도 프레임 구조와 주소 의미가 크게 달라짐을 보여 줍니다. |
| [`TLS Packet Analysis`](tls-ssl/README.md) | `Computer Networking: A Top-Down Approach`의 TLS/SSL Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 | `analysis/src/` | `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test` | `verified` | top-down 순서의 마지막에서 보안 프로토콜이 transport 위에 어떻게 올라가는지 정리하며, 암호화 이후 무엇이 보이고 무엇이 보이지 않는지도 함께 보여 줍니다. |

## 공통 읽기 순서

1. 프로젝트 README에서 문제, 답, 검증 명령을 먼저 확인합니다.
2. `problem/README.md`에서 제공 자료와 성공 기준을 확인합니다.
3. 구현형 과제는 `python/README.md` 또는 `cpp/README.md`, 분석형 과제는 `analysis/README.md`로 내려갑니다.
4. `docs/README.md`는 개념을 다시 확인할 때만 참고하고, `notion/README.md`는 보조 기록으로만 읽습니다.

## 단계 공통 검증

- `make -C study/03-Packet-Analysis-Top-Down test`
