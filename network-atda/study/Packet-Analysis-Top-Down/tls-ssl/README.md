# TLS Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 TLS/SSL Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/tls-ssl/problem test` |

## 한 줄 요약

TLS handshake, certificate, cipher suite, 버전 차이를 record/message 수준에서 읽는 보안 랩입니다.

## 왜 이 프로젝트가 필요한가

top-down 순서의 마지막에서 보안 프로토콜이 transport 위에 어떻게 올라가는지 정리하며, 암호화 이후 무엇이 보이고 무엇이 보이지 않는지도 함께 보여 줍니다.

## 이런 학습자에게 맞습니다

- TLS handshake 흐름과 certificate chain을 trace로 이해하고 싶은 학습자
- TLS 1.2와 1.3의 메시지 차이를 실제 trace에서 확인하고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 질문 목록과 trace 범위를 먼저 확인합니다.
2. `analysis/README.md` - 공개 답안이 어떤 evidence 원칙으로 작성되는지 확인합니다.
3. `docs/README.md` - 개념 문서 중 지금 필요한 부분만 다시 읽습니다.

## 제공 자료

- `problem/data/tls-trace.pcap`: TLS handshake와 암호화된 데이터가 담긴 trace
- `analysis/src/tls-ssl-analysis.md`: 공개 답안
- `docs/concepts/tls-protocol.md`: TLS 개념 문서

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/tls-ssl/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 학습 포인트

- ClientHello/ServerHello 순서 해석
- cipher suite 의미
- certificate chain과 가시성 한계
- TLS 1.2 vs 1.3의 RTT/메시지 차이

## 현재 한계

- 제공 trace가 minimal synthetic capture라 일부 certificate detail과 extension은 제한적입니다.
- decryption 실습은 필수 범위에 넣지 않았습니다.

## 포트폴리오로 확장하기

- TLS 1.2와 1.3 비교 표를 스스로 정리하면 문서 품질이 좋아집니다.
- 복호화 실습을 별도 부록으로 붙이면 보안 학습의 깊이를 더 잘 보여 줄 수 있습니다.
- HTTP trace와 TLS trace를 연결해 같은 애플리케이션 데이터가 보안 계층 위에서 어떻게 달라지는지 설명하면 좋습니다.
