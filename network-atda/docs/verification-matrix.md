# Verification Matrix

아래 표는 `2026-03-10` 기준 현재 저장소에서 확인하는 canonical 검증 명령을 모아 둔 것입니다.

| 프로젝트 | 상태 | Canonical 검증 | 비고 |
| :--- | :--- | :--- | :--- |
| `Application-Protocols-and-Sockets/web-server` | `verified` | `make -C study/Application-Protocols-and-Sockets/web-server/problem test` | 별도 `pytest`는 서버 선기동이 필요하므로 보조 검증으로만 취급합니다. |
| `Application-Protocols-and-Sockets/udp-pinger` | `verified` | `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem test` | 제공 서버를 포함한 통합 흐름을 우선 검증합니다. |
| `Application-Protocols-and-Sockets/smtp-client` | `verified` | `make -C study/Application-Protocols-and-Sockets/smtp-client/problem test` | 로컬 mock SMTP 서버를 포함한 정식 흐름을 사용합니다. |
| `Application-Protocols-and-Sockets/web-proxy` | `verified` | `make -C study/Application-Protocols-and-Sockets/web-proxy/problem test` | origin fetch와 cache hit를 함께 확인합니다. |
| `Reliable-Transport/rdt-protocol` | `verified` | `make -C study/Reliable-Transport/rdt-protocol/problem test` | `rdt3.0`, `GBN` 전송이 모두 통과해야 합니다. |
| `Reliable-Transport/selective-repeat` | `verified` | `make -C study/Reliable-Transport/selective-repeat/problem test` | 공유 helper를 재사용하면서 SR 흐름을 검증합니다. |
| `Network-Diagnostics-and-Routing/icmp-pinger` | `verified` | `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test` | raw socket이 아닌 deterministic test를 기준으로 판정합니다. live 실행은 보조 경로입니다. |
| `Network-Diagnostics-and-Routing/traceroute` | `verified` | `make -C study/Network-Diagnostics-and-Routing/traceroute/problem test` | parser/formatter와 synthetic hop integration을 함께 확인합니다. |
| `Network-Diagnostics-and-Routing/routing` | `verified` | `make -C study/Network-Diagnostics-and-Routing/routing/problem test` | 3노드와 5노드 토폴로지 수렴을 모두 확인합니다. |
| `Packet-Analysis-Top-Down/http` | `verified` | `make -C study/Packet-Analysis-Top-Down/http/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `Packet-Analysis-Top-Down/dns` | `verified` | `make -C study/Packet-Analysis-Top-Down/dns/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `Packet-Analysis-Top-Down/tcp-udp` | `verified` | `make -C study/Packet-Analysis-Top-Down/tcp-udp/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `Packet-Analysis-Top-Down/ip-icmp` | `verified` | `make -C study/Packet-Analysis-Top-Down/ip-icmp/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `Packet-Analysis-Top-Down/ethernet-arp` | `verified` | `make -C study/Packet-Analysis-Top-Down/ethernet-arp/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `Packet-Analysis-Top-Down/wireless-802.11` | `verified` | `make -C study/Packet-Analysis-Top-Down/wireless-802.11/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `Packet-Analysis-Top-Down/tls-ssl` | `verified` | `make -C study/Packet-Analysis-Top-Down/tls-ssl/problem test` | `analysis/src/` 답안 완결성을 확인합니다. |
| `Packet-Analysis-Top-Down (aggregate)` | `verified` | `make -C study/Packet-Analysis-Top-Down test` | 7개 랩 전체 검증 |
| `Game-Server-Capstone/tactical-arena-server` | `verified` | `make -C study/Game-Server-Capstone/tactical-arena-server/problem test` | `C++20 + Boost.Asio + SQLite + CMake/CTest` 기반 capstone. unit + integration + load smoke를 한 번에 확인합니다. |
