# TLS Packet Analysis blog

`TLS Packet Analysis` 문서 묶음은 암호화 이후에도 TLS handshake에서 무엇은 보이고 무엇은 숨는가?라는 질문에 답하기 위해 준비한 읽기 경로다. 결과만 요약하지 않고, 어디서부터 구현이나 분석이 무거워졌는지 따라갈 수 있게 구성했다.

이 프로젝트의 본문은 `TLS handshake, certificate, cipher suite, 버전 차이를 record/message 수준에서 읽는 보안 랩입니다.`라는 한 줄 설명을 실제 파일, CLI, 테스트 신호로 다시 풀어 쓰는 데 초점을 둔다.

## 이 폴더에서 기대할 수 있는 것

- 문제 경계와 읽는 순서: [00-series-map.md](00-series-map.md)
- 단계별 근거 압축본: [01-evidence-ledger.md](01-evidence-ledger.md)
- 글의 편집 개요: [02-structure.md](02-structure.md)
- 실제 서사형 기록: [10-development-timeline.md](10-development-timeline.md)

## 근거로 사용한 source set

- 프로젝트 루트: `study/03-Packet-Analysis-Top-Down/tls-ssl`
- 정식 검증 명령: `make -C study/03-Packet-Analysis-Top-Down/tls-ssl/problem test`
- 분석 본문: `study/03-Packet-Analysis-Top-Down/tls-ssl/analysis/src/tls-ssl-analysis.md`
- 제외한 입력: 기존 `study/blog/**`, `notion/**`, `notion-archive/**`

## 먼저 읽을 순서

1. `00-series-map.md`에서 질문과 근거를 먼저 잡는다.
2. `01-evidence-ledger.md`에서 세 단계 흐름을 짧게 본다.
3. `10-development-timeline.md`에서 코드/trace와 CLI를 따라 내려간다.
