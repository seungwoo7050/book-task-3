# TLS Packet Analysis structure guide

## 이 글의 중심 질문

- 암호화 이후에도 TLS handshake에서 무엇은 보이고 무엇은 숨는가?
- 한 줄 답: TLS handshake, certificate, cipher suite, 버전 차이를 record/message 수준에서 읽는 보안 랩입니다.

## 권장 흐름

1. 질문과 trace 범위를 먼저 세우기
2. ClientHello와 ServerHello/Certificate를 handshake 축으로 묶기
3. verify 스크립트와 한계까지 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test`
- `study/03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`의 `## Part 2: ServerHello and Certificate (Q6–Q11)`
- `study/03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`의 `## Part 3: ChangeCipherSpec and Application Data (Q12–Q16)`

## 리라이트 주의점

- `TLS Packet Analysis`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 제공 trace가 minimal synthetic capture라 일부 certificate detail과 extension은 제한적입니다. 같은 남은 경계를 사람 말로 다시 정리한다.
