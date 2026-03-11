# HTTP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 문제 배경 | `Computer Networking: A Top-Down Approach`의 HTTP Wireshark 랩을 현재 저장소의 `problem/analysis/docs` 구조로 재정리한 프로젝트 |
| 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/http/problem test` |

## 문제가 뭐였나
- 문제 배경: `Computer Networking: A Top-Down Approach`의 HTTP Wireshark 랩을 현재 저장소의 `problem/analysis/docs` 구조로 재정리한 프로젝트
- 이 단계에서의 역할: 사람이 읽을 수 있는 텍스트 프로토콜인 HTTP를 시작점으로 삼아, Wireshark로 무엇을 관찰하고 어떤 근거로 설명해야 하는지 감을 잡기 좋습니다.

## 제공된 자료
- `problem/data/http-basic.pcapng`: 기본 GET 시나리오 trace
- `problem/data/http-conditional.pcapng`: conditional GET trace
- `problem/data/http-long-document.pcapng`: 긴 문서 전송 trace
- `problem/data/http-embedded-objects.pcapng`: 여러 객체가 포함된 페이지 trace
- `analysis/src/http-analysis.md`: 공개 답안

## 이 레포의 답
- 한 줄 답: 기본 GET, conditional GET, 긴 문서 전송, embedded object 요청을 패킷 수준에서 추적하는 랩입니다.
- 공개 답안 위치: `analysis/src/`
- 보조 공개 표면: `docs/`
- 읽는 순서:
  1. `problem/README.md` - 문제 조건, 제공 자료, 성공 기준을 먼저 확인합니다.
  2. `analysis/README.md` - 현재 공개 답안 범위와 기준 명령을 확인합니다.
  3. `docs/README.md` - 반복해서 참고할 개념 문서를 고릅니다.

## 어떻게 검증하나
- 검증: `make -C study/03-Packet-Analysis-Top-Down/http/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 무엇을 배웠나
- HTTP 상태 코드 해석
- `If-Modified-Since`와 `304 Not Modified`
- 긴 응답이 여러 TCP segment로 나뉘는 모습
- embedded object 요청 체인

## 현재 한계
- `HTTP/2` 이상은 다루지 않습니다.
- 브라우저별 헤더 차이는 관찰 범위 밖입니다.
- 실시간 캡처 대신 고정 trace에 기반합니다.
