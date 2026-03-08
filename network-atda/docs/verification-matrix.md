# Verification Matrix

| 프로젝트 | 상태 | Canonical 검증 | 비고 |
| :--- | :--- | :--- | :--- |
| `Application-Protocols-and-Sockets/web-server` | `verified` | `make -C study/Application-Protocols-and-Sockets/web-server/problem test` | 별도 pytest는 서버 선기동이 필요하므로 보조 검증으로만 취급합니다. |
| `Application-Protocols-and-Sockets/udp-pinger` | `verified` | `make -C study/Application-Protocols-and-Sockets/udp-pinger/problem test` | pytest 파일은 여전히 서버 선기동을 전제로 하므로 주 검증은 `make test`입니다. |
| `Application-Protocols-and-Sockets/smtp-client` | `verified` | `make -C study/Application-Protocols-and-Sockets/smtp-client/problem test` | 보조 pytest는 로컬 SMTP 서버 선기동이 필요합니다. |
| `Application-Protocols-and-Sockets/web-proxy` | `verified` | `make -C study/Application-Protocols-and-Sockets/web-proxy/problem test` | 단위 테스트는 URL 파싱과 캐시 키 생성만 검증하는 보조 수단입니다. |
| `Reliable-Transport/rdt-protocol` | `verified` | `make -C study/Reliable-Transport/rdt-protocol/problem test` | 새 구조에서는 `python/src`가 어디서 실행되든 `problem/code`와 `problem/data`를 찾도록 경로를 고정했습니다. |
| `Reliable-Transport/selective-repeat` | `verified` | `make -C study/Reliable-Transport/selective-repeat/problem test` | 문제 보조 모듈은 기존 `rdt-protocol`의 packet/channel 계약을 그대로 재사용합니다. |
| `Network-Diagnostics-and-Routing/icmp-pinger` | `verified` | `make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test` | checksum, packet build, synthetic raw-socket flow를 deterministic pytest로 검증합니다. `sudo make -C study/Network-Diagnostics-and-Routing/icmp-pinger/problem test-live HOST=google.com`은 수동 live 재현용입니다. |
| `Network-Diagnostics-and-Routing/traceroute` | `verified` | `make -C study/Network-Diagnostics-and-Routing/traceroute/problem test` | parser/formatter와 synthetic hop integration을 함께 검증합니다. `make ... run-client`는 네트워크 환경에 따라 결과가 달라지는 수동 재현 경로입니다. |
| `Network-Diagnostics-and-Routing/routing` | `verified` | `make -C study/Network-Diagnostics-and-Routing/routing/problem test` | 테스트와 단위 검증 모두 새 `python/src` 경로를 기준으로 정리했습니다. |
| `Packet-Analysis-Top-Down/http` | `verified` | `make -C study/Packet-Analysis-Top-Down/http/problem test` | 답안 완결성 스크립트를 `analysis/src/` 기준으로 래핑 |
| `Packet-Analysis-Top-Down/dns` | `verified` | `make -C study/Packet-Analysis-Top-Down/dns/problem test` | 답안 완결성 스크립트를 `analysis/src/` 기준으로 래핑 |
| `Packet-Analysis-Top-Down/tcp-udp` | `verified` | `make -C study/Packet-Analysis-Top-Down/tcp-udp/problem test` | 답안 완결성 스크립트를 `analysis/src/` 기준으로 래핑 |
| `Packet-Analysis-Top-Down/ip-icmp` | `verified` | `make -C study/Packet-Analysis-Top-Down/ip-icmp/problem test` | 답안 완결성 스크립트를 `analysis/src/` 기준으로 래핑 |
| `Packet-Analysis-Top-Down/ethernet-arp` | `verified` | `make -C study/Packet-Analysis-Top-Down/ethernet-arp/problem test` | 답안 완결성 스크립트를 `analysis/src/` 기준으로 래핑 |
| `Packet-Analysis-Top-Down/wireless-802.11` | `verified` | `make -C study/Packet-Analysis-Top-Down/wireless-802.11/problem test` | 답안 완결성 스크립트를 `analysis/src/` 기준으로 래핑 |
| `Packet-Analysis-Top-Down/tls-ssl` | `verified` | `make -C study/Packet-Analysis-Top-Down/tls-ssl/problem test` | 답안 완결성 스크립트를 `analysis/src/` 기준으로 래핑 |
| `Packet-Analysis-Top-Down (aggregate)` | `verified` | `make -C study/Packet-Analysis-Top-Down test` | 7개 랩 전체 검증 |
| `Game-Server-Capstone/tactical-arena-server` | `verified` | `make -C study/Game-Server-Capstone/tactical-arena-server/problem test` | `C++20 + Boost.Asio + SQLite + CMake/CTest` capstone. unit + integration + load smoke를 한 명령으로 검증합니다. |
