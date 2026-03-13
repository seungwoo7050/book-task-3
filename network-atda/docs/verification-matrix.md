# Verification Matrix

아래 표는 현재 저장소에서 확인하는 canonical 검증 명령을 모아 둔 것입니다.

| 프로젝트 | 상태 | Canonical 검증 | 비고 |
| :--- | :--- | :--- | :--- |
| `01-Application-Protocols-and-Sockets/web-server` | `verified` | `make -C study/01-Application-Protocols-and-Sockets/web-server/problem test` | 공개 구현과 보조 테스트가 현재 범위 안에서 동작하는지 확인합니다. |
| `01-Application-Protocols-and-Sockets/udp-pinger` | `verified` | `make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test` | 공개 구현과 보조 테스트가 현재 범위 안에서 동작하는지 확인합니다. |
| `01-Application-Protocols-and-Sockets/smtp-client` | `verified` | `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test` | 공개 구현과 보조 테스트가 현재 범위 안에서 동작하는지 확인합니다. |
| `01-Application-Protocols-and-Sockets/web-proxy` | `verified` | `make -C study/01-Application-Protocols-and-Sockets/web-proxy/problem test` | 공개 구현과 보조 테스트가 현재 범위 안에서 동작하는지 확인합니다. |
| `02-Reliable-Transport/rdt-protocol` | `verified` | `make -C study/02-Reliable-Transport/rdt-protocol/problem test` | 공개 구현과 보조 테스트가 현재 범위 안에서 동작하는지 확인합니다. |
| `02-Reliable-Transport/selective-repeat` | `verified` | `make -C study/02-Reliable-Transport/selective-repeat/problem test` | 공개 구현과 보조 테스트가 현재 범위 안에서 동작하는지 확인합니다. |
| `03-Packet-Analysis-Top-Down/http` | `verified` | `make -C study/03-Packet-Analysis-Top-Down/http/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `03-Packet-Analysis-Top-Down/dns` | `verified` | `make -C study/03-Packet-Analysis-Top-Down/dns/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `03-Packet-Analysis-Top-Down/tcp-udp` | `verified` | `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `03-Packet-Analysis-Top-Down/ip-icmp` | `verified` | `make -C study/03-Packet-Analysis-Top-Down/ip-icmp/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `03-Packet-Analysis-Top-Down/ethernet-arp` | `verified` | `make -C study/03-Packet-Analysis-Top-Down/ethernet-arp/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `03-Packet-Analysis-Top-Down/wireless-802.11` | `verified` | `make -C study/03-Packet-Analysis-Top-Down/wireless-802.11/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `03-Packet-Analysis-Top-Down/tls-ssl` | `verified` | `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `03-Packet-Analysis-Top-Down/http2-quic` | `verified` | `make -C study/03-Packet-Analysis-Top-Down/http2-quic/problem test` | `analysis/src/` 답안 완결성과 trace TSV 일치를 확인합니다. |
| `04-Network-Diagnostics-and-Routing/icmp-pinger` | `verified` | `make -C study/04-Network-Diagnostics-and-Routing/icmp-pinger/problem test` | 공개 구현과 보조 테스트가 현재 범위 안에서 동작하는지 확인합니다. |
| `04-Network-Diagnostics-and-Routing/traceroute` | `verified` | `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test` | 공개 구현과 보조 테스트가 현재 범위 안에서 동작하는지 확인합니다. |
| `04-Network-Diagnostics-and-Routing/routing` | `verified` | `make -C study/04-Network-Diagnostics-and-Routing/routing/problem test` | 공개 구현과 보조 테스트가 현재 범위 안에서 동작하는지 확인합니다. |
| `05-Game-Server-Capstone/tactical-arena-server` | `verified` | `make -C study/05-Game-Server-Capstone/tactical-arena-server/problem test` | 공개 구현과 보조 테스트가 현재 범위 안에서 동작하는지 확인합니다. |
| `03-Packet-Analysis-Top-Down (aggregate)` | `verified` | `make -C study/03-Packet-Analysis-Top-Down test` | 8개 랩 전체 검증 |
