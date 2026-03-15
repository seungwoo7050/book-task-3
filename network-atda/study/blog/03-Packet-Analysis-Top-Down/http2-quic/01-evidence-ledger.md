# HTTP/2 and QUIC Packet Analysis Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/03-Packet-Analysis-Top-Down/http2-quic/problem/README.md`
- 답안 엔트리: `study/03-Packet-Analysis-Top-Down/http2-quic/analysis/src/http2-quic-analysis.md`
- 검증 스크립트: `study/03-Packet-Analysis-Top-Down/http2-quic/problem/script/verify_answers.sh`
- 실행 표면: `study/03-Packet-Analysis-Top-Down/http2-quic/problem/Makefile`

## 핵심 근거

- `compare` 출력의 HTTP/2 section:
  - frame `18` stream `1` `HEADERS` `GET /feed`
  - frame `19` stream `3` `HEADERS` `GET /avatars/42.png`
  - frames `20/21/23/24`가 두 stream의 DATA를 교차시킨다
  - frame `22` stream `0` `WINDOW_UPDATE`
- `compare` 출력의 QUIC section:
  - frames `31-34` `Initial/Handshake`
  - frames `35-39` `1-RTT`
  - connection IDs `8394c8f03e515708`, `1f4a7b9c00112233`
  - application streams `4`, `8`
- `analysis/src/http2-quic-analysis.md`는 HTTP/2 HOL 한계와 QUIC transport-level multiplexing 차이를 비교 결론으로 고정한다.

## 테스트 근거

`make -C network-atda/study/03-Packet-Analysis-Top-Down/http2-quic/problem test`

결과:

- `PASS: http2-quic answer file passed content verification`

## 이번에 고정한 해석

- 이 lab는 packet dissector detail보다 architecture comparison을 위한 dataset 읽기 랩이다.
- HTTP/2는 application streams를 interleave하지만, TCP segment 하나의 손실이 connection 전체를 막을 수 있다는 점에서 HOL 문제를 완전히 지우지 못한다.
- QUIC의 핵심 신호는 `UDP`라는 사실 자체보다, packet number와 connection ID가 transport-level state를 노출한다는 데 있다.
