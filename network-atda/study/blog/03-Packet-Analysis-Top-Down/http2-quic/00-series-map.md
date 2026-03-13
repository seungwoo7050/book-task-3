# HTTP/2 and QUIC Packet Analysis series map

이 프로젝트를 읽을 때 붙들 질문은 하나다. HTTP/2와 QUIC은 모두 여러 stream을 다루지만, 왜 head-of-line의 위치가 달라지는가?

## 무엇을 근거로 복원했는가

- 프로젝트 README: `study/03-Packet-Analysis-Top-Down/http2-quic/README.md`
- 문제 문서와 실행 표면: `study/03-Packet-Analysis-Top-Down/http2-quic/problem/README.md`, `study/03-Packet-Analysis-Top-Down/http2-quic/problem/Makefile`
- 분석 본문: `study/03-Packet-Analysis-Top-Down/http2-quic/analysis/src/http2-quic-analysis.md`
- 정식 검증 출력: `make -C study/03-Packet-Analysis-Top-Down/http2-quic/problem test`

## 어떤 순서로 읽으면 되는가

1. `problem/README.md`로 질문 12개를 먼저 확인한다.
2. `01-evidence-ledger.md`로 비교 포인트를 짧게 잡는다.
3. `10-development-timeline.md`에서 stream, packet type, connection ID를 따라간다.
