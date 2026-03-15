# http2-quic 문제지

## 왜 중요한가

이 문서는 HTTP/2 and QUIC Packet Analysis를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. raw pcap을 모두 들여다보기보다, trace에서 뽑아 낸 condensed dataset을 근거로 비교 포인트를 분명하게 잡는 데 초점을 둡니다.

## 목표

시작 위치의 구현을 완성해 총 12개 질문에 모두 답한다, frame 번호, stream ID, packet type, connection ID 같은 근거를 직접 적는다, HTTP/2와 QUIC의 차이를 단순 "더 빠르다"가 아니라 구조 차이로 설명한다를 한 흐름으로 설명하고 검증한다.

## 시작 위치

- `../study/03-Packet-Analysis-Top-Down/http2-quic/problem/data/http2-trace.tsv`
- `../study/03-Packet-Analysis-Top-Down/http2-quic/problem/data/quic-trace.tsv`
- `../study/03-Packet-Analysis-Top-Down/http2-quic/problem/data/tls-trace.pcap`
- `../study/03-Packet-Analysis-Top-Down/http2-quic/problem/Makefile`

## starter code / 입력 계약

- `../study/03-Packet-Analysis-Top-Down/http2-quic/problem/data/http2-trace.tsv`부터 읽으면 가장 짧게 구현을 시작할 수 있다.

## 핵심 요구사항

- 총 12개 질문에 모두 답한다.
- frame 번호, stream ID, packet type, connection ID 같은 근거를 직접 적는다.
- HTTP/2와 QUIC의 차이를 단순 "더 빠르다"가 아니라 구조 차이로 설명한다.

## 제외 범위

- `../study/03-Packet-Analysis-Top-Down/http2-quic/problem/data/http2-trace.tsv` 등 fixture나 trace를 읽지 않고 동작을 추측해서 구현하지 않는다.
- 상위 카탈로그 요약만 보고 세부 산출물 계약을 생략하지 않는다.
- 검증 명령이 통과한다고 해서 입력 계약과 경계 조건까지 자동으로 맞는다고 가정하지 않는다.

## 성공 체크리스트

- `../study/03-Packet-Analysis-Top-Down/http2-quic/problem/data/http2-trace.tsv` 등 fixture/trace 기준으로 결과를 대조했다.
- `make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/http2-quic/problem test`가 통과한다.

## 검증 방법

```bash
make -C /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/http2-quic/problem test
```

```bash
bash /Users/woopinbell/work/book-task-3/network-atda/study/03-Packet-Analysis-Top-Down/http2-quic/problem/script/verify_answers.sh
```

- `http2-quic`의 Makefile이 호출하는 하위 toolchain이 현재 셸에서 동작해야 한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`http2-quic_answer.md`](http2-quic_answer.md)에서 확인한다.
