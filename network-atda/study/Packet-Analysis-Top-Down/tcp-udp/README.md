# TCP and UDP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Wireshark-Labs/tcp-udp` |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/tcp-udp/problem test` |

## 한 줄 요약

TCP의 신뢰성 메커니즘과 UDP의 단순성을 같은 전송 계층 시야에서 비교하는 랩이다.

## 문제 요약

TCP handshake, seq/ack 증가, retransmission, window advertisement, UDP header를 trace에서 관찰해 전송 계층 trade-off를 정리한다.

## 이 프로젝트를 여기 둔 이유

응용 계층 랩 다음에 전송 계층의 상태와 오버헤드를 비교하며, 이후 RDT 구현 과제와도 연결되는 관찰 기반을 만든다.

## 제공 자료

- `problem/data/tcp-upload.pcapng`
- `problem/data/udp-dns.pcapng`
- `analysis/src/tcp-udp-analysis.md`

## 학습 포인트

- 3-way handshake 해석
- relative seq/ack 읽기
- window field와 retransmission 표시
- UDP의 8-byte header와 무상태성

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/tcp-udp/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 현재 범위와 한계

trace가 짧아 전체 congestion window evolution은 직접 관찰되지 않는다.

- 현재 한계: cwnd는 간접 추정만 가능
- 현재 한계: trace 길이가 짧아 teardown과 장기 혼잡 제어는 제한적

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
