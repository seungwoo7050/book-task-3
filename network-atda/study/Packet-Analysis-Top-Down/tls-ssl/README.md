# TLS Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Wireshark-Labs/tls-ssl` |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/tls-ssl/problem test` |

## 한 줄 요약

TLS handshake, certificate, cipher suite, 버전 차이를 record/message 수준에서 읽는 보안 랩이다.

## 문제 요약

ClientHello, ServerHello, Certificate, ChangeCipherSpec, Application Data를 trace에서 관찰하며 TLS 1.2와 1.3 차이를 정리한다.

## 이 프로젝트를 여기 둔 이유

top-down 순서의 마지막에서 보안 프로토콜이 transport 위에 어떻게 얹히는지 정리하며, 가시성과 비가시성의 경계를 보여준다.

## 제공 자료

- `problem/data/tls-trace.pcap`
- `analysis/src/tls-ssl-analysis.md`
- `docs/concepts/tls-protocol.md`

## 학습 포인트

- ClientHello/ServerHello 순서 해석
- cipher suite 의미
- certificate visibility 한계
- TLS 1.2 vs 1.3 RTT 차이

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/tls-ssl/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 현재 범위와 한계

제공 trace가 minimal synthetic capture라 certificate detail과 일부 extension은 직접 관찰되지 않는다.

- 현재 한계: certificate detail 일부 malformed
- 현재 한계: decryption 실습은 포함하지 않음

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
