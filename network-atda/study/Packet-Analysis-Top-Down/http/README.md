# HTTP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 HTTP Wireshark 랩을 현재 저장소의 `problem/analysis/docs` 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/http/problem test` |

## 한 줄 요약

기본 GET, conditional GET, 긴 문서 전송, embedded object 요청을 패킷 수준에서 추적하는 랩입니다.

## 왜 이 프로젝트가 필요한가

사람이 읽을 수 있는 텍스트 프로토콜인 HTTP를 시작점으로 삼아, Wireshark로 무엇을 관찰하고 어떤 근거로 설명해야 하는지 감을 잡기 좋습니다.

## 이런 학습자에게 맞습니다

- Wireshark를 처음 학습하면서 텍스트 기반 프로토콜부터 읽고 싶은 학습자
- 패킷 분석 답안을 근거 중심으로 작성하는 연습이 필요한 학습자

## 지금 바로 읽는 순서

1. `problem/README.md` - 질문 목록과 trace 범위를 먼저 확인합니다.
2. `analysis/README.md` - 공개 답안이 어떤 evidence 원칙으로 작성되는지 확인합니다.
3. `docs/README.md` - 개념 문서 중 지금 필요한 부분만 다시 읽습니다.

## 제공 자료

- `problem/data/http-basic.pcapng`: 기본 GET 시나리오 trace
- `problem/data/http-conditional.pcapng`: conditional GET trace
- `problem/data/http-long-document.pcapng`: 긴 문서 전송 trace
- `problem/data/http-embedded-objects.pcapng`: 여러 객체가 포함된 페이지 trace
- `analysis/src/http-analysis.md`: 공개 답안

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/http/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 학습 포인트

- HTTP 상태 코드 해석
- `If-Modified-Since`와 `304 Not Modified`
- 긴 응답이 여러 TCP segment로 나뉘는 모습
- embedded object 요청 체인

## 현재 한계

- `HTTP/2` 이상은 다루지 않습니다.
- 브라우저별 헤더 차이는 관찰 범위 밖입니다.
- 실시간 캡처 대신 고정 trace에 기반합니다.

## 포트폴리오로 확장하기

- packet/frame 번호와 함께 해석 스크린샷을 넣으면 학습 노트가 좋은 분석 포트폴리오로 바뀝니다.
- 같은 질문을 다른 웹사이트 trace에 다시 적용해 본 결과를 추가하면 차별화가 됩니다.
- HTTP 구현 프로젝트(`web-server`, `web-proxy`)와 연결해 직접 구현한 프로토콜을 trace에서 다시 읽는 스토리를 만들면 좋습니다.
