# HTTP Packet Analysis

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Wireshark-Labs/http` |
| 정식 검증 | `make -C study/Packet-Analysis-Top-Down/http/problem test` |

## 한 줄 요약

기본 GET, conditional GET, 긴 문서 전송, embedded object 요청을 패킷 수준에서 추적하는 랩이다.

## 문제 요약

제공된 HTTP pcap을 열어 요청/응답 헤더, 상태 코드, 조건부 캐시 헤더, TCP reassembly, embedded object fetch 순서를 해석한다.

## 이 프로젝트를 여기 둔 이유

top-down 순서의 첫 랩으로, 사람이 읽을 수 있는 텍스트 프로토콜을 Wireshark 분석 습관의 시작점으로 삼는다.

## 제공 자료

- `problem/data/http-*.pcapng` traces
- `problem/script/verify_answers.sh`
- `analysis/src/http-analysis.md` 공개 답안

## 학습 포인트

- HTTP 상태 코드 해석
- conditional GET과 304 Not Modified
- 장문 응답의 TCP segment 분할
- embedded object 요청 체인

## 실행과 검증

- 검증: `make -C study/Packet-Analysis-Top-Down/http/problem test`
- 공개 답안 위치: `analysis/src/`
- 개념 노트 위치: `docs/concepts/`

## 현재 범위와 한계

trace가 고정되어 있으므로 답안은 제공된 프레임 범위 안에서만 주장한다.

- 현재 한계: HTTP/2 이상은 다루지 않음
- 현재 한계: 브라우저별 헤더 차이는 관찰 범위 밖
- 현재 한계: 실시간 캡처 대신 재현 trace 중심

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
