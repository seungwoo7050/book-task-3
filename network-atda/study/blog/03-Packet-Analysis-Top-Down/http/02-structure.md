# HTTP Packet Analysis structure guide

## 이 글의 중심 질문

- HTTP trace에서 질문 하나마다 어떤 frame과 header를 근거로 답해야 하는가?
- 한 줄 답: 기본 GET, conditional GET, 긴 문서 전송, embedded object 요청을 패킷 수준에서 추적하는 랩입니다.

## 권장 흐름

1. 질문과 trace 범위를 먼저 세우기
2. 기본 GET과 conditional GET을 frame 근거로 채우기
3. verify 스크립트와 한계까지 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/03-Packet-Analysis-Top-Down/http/problem test`
- `study/03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`의 `## Part 2: Conditional GET`
- `study/03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`의 `## Part 3: Long Documents`

## 리라이트 주의점

- `HTTP Packet Analysis`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 `HTTP/2` 이상은 다루지 않습니다. 같은 남은 경계를 사람 말로 다시 정리한다.
