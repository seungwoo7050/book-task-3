# TCP and UDP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 TCP/UDP Wireshark 랩을 현재 저장소 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/tcp-udp/problem test` |

## 한 줄 요약

TCP의 신뢰성 메커니즘과 UDP의 단순성을 같은 전송 계층 시야에서 비교하는 랩입니다.

## 왜 이 프로젝트가 필요한가

응용 계층 랩 다음에 전송 계층의 상태와 오버헤드를 직접 관찰하면서, 이후 신뢰 전송 구현 트랙과 연결되는 근거를 쌓을 수 있습니다.

## 이런 학습자에게 맞습니다

- TCP handshake, ACK, retransmission, window가 실제 trace에서 어떻게 보이는지 확인하고 싶은 학습자
- UDP 헤더가 얼마나 단순한지 비교하며 이해하고 싶은 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 질문 목록과 trace 범위를 먼저 확인합니다.
2. `analysis/README.md` - 공개 답안이 어떤 evidence 원칙으로 작성되는지 확인합니다.
3. `docs/README.md` - 개념 문서 중 지금 필요한 부분만 다시 읽습니다.

## 제공 자료

- `problem/data/tcp-upload.pcapng`: HTTP POST 업로드가 담긴 TCP trace
- `problem/data/udp-dns.pcapng`: DNS 질의/응답이 담긴 UDP trace
- `analysis/src/tcp-udp-analysis.md`: 공개 답안

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/tcp-udp/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 학습 포인트

- 3-way handshake 해석
- relative sequence/ack 읽기
- window field와 retransmission 표시
- UDP의 8-byte header와 무상태성

## 현재 한계

- trace가 짧아 전체 congestion window evolution을 직접 보기는 어렵습니다.
- teardown과 장기 혼잡 제어 관찰은 제한적입니다.

## 포트폴리오로 확장하기

- TCP stream graph 캡처와 계산 메모를 함께 넣으면 분석 포트폴리오 품질이 좋아집니다.
- 신뢰 전송 구현 트랙과 연결해 코드로 만든 개념을 trace에서 다시 확인했다는 흐름을 만들 수 있습니다.
- 같은 질문을 다른 TCP trace에 재적용한 결과를 추가하면 훨씬 차별화됩니다.
