# TLS Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 TLS/SSL Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 TLS/SSL Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트
- 이 단계에서의 역할: top-down 순서의 마지막에서 보안 프로토콜이 transport 위에 어떻게 올라가는지 정리하며, 암호화 이후 무엇이 보이고 무엇이 보이지 않는지도 함께 보여 줍니다.

## 제공된 자료
- `problem/data/tls-trace.pcap`: TLS handshake와 암호화된 데이터가 담긴 trace
- `analysis/src/tls-ssl-analysis.md`: 공개 답안
- `docs/concepts/tls-protocol.md`: TLS 개념 문서

## 이 레포의 답
- 한 줄 답: TLS handshake, certificate, cipher suite, 버전 차이를 record/message 수준에서 읽는 보안 랩입니다.
- 공개 답안 위치: `analysis/src/`
- 보조 공개 표면: `docs/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `analysis/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.

## 어떻게 검증하나
- 검증: `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 무엇을 배웠나
- ClientHello/ServerHello 순서 해석
- cipher suite 의미
- certificate chain과 가시성 한계
- TLS 1.2 vs 1.3의 RTT/메시지 차이

## 현재 한계
- 제공 trace가 minimal synthetic capture라 일부 certificate detail과 extension은 제한적입니다.
- decryption 실습은 필수 범위에 넣지 않았습니다.
