# TLS Packet Analysis 시리즈 지도

## 이 프로젝트를 한 줄로

TLS를 "복잡한 암호 프로토콜"로 뭉개지 않고, capture에 실제로 보이는 handshake 순서와 보이지 않는 certificate detail의 경계를 기록한 글이다.

## 시작 전에 고정한 자료

- 제공 trace: `problem/data/tls-trace.pcap`
- 실행 진입점: `problem/Makefile`
- 사용자 답안: `study/03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`
- 보조 개념 문서: `docs/concepts/wireshark-tls.md`

## 이 시리즈에서 따라갈 질문

1. ClientHello, ServerHello, Certificate, ChangeCipherSpec, Application Data는 어떤 frame 순서로 등장하는가.
2. ClientHello와 ServerHello에서 TLS version, cipher suite, extension 존재 여부를 어디까지 확정할 수 있는가.
3. Certificate가 malformed로 보일 때 subject, issuer, validity를 어디서 멈춰야 하는가.
4. 암호화 이후에도 packet에서 여전히 보이는 메타데이터는 무엇이고, 더 이상 볼 수 없는 것은 무엇인가.

## 검증 명령

- handshake 전체: `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem handshake`
- ClientHello: `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem client-hello`
- ServerHello: `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem server-hello`
- Certificate: `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem certs`
- record 요약: `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem records`
- 답안 검증: `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test`

## 글 구성

| 파일 | 역할 |
| :--- | :--- |
| `00-series-map.md` | handshake 순서와 관찰 한계를 먼저 선언한다. |
| `10-development-timeline.md` | Hello 메시지 확인 → certificate 한계 인식 → encrypted record 해석 순으로 진행한다. |
