# DNS Packet Analysis structure guide

## 이 글의 중심 질문

- DNS trace에서 query, response, authoritative 여부를 어떤 필드로 구분했는가?
- 한 줄 답: DNS query/response 구조와 TTL 기반 캐시를 Wireshark로 해석하는 랩입니다.

## 권장 흐름

1. 질문과 trace 범위를 먼저 세우기
2. query/response 흐름과 권한 정보를 필드 단위로 확인하기
3. verify 스크립트와 한계까지 정리하기

## 꼭 살릴 근거

- `problem/Makefile`의 공개 target과 `make -C study/03-Packet-Analysis-Top-Down/dns/problem test`
- `study/03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`의 `## Part 2: Authoritative and Non-Authoritative`
- `study/03-Packet-Analysis-Top-Down/dns/analysis/src/dns-analysis.md`의 `## Part 3: DNS Responses and Records`

## 리라이트 주의점

- `DNS Packet Analysis`를 개념 강의처럼 풀지 말고, 실제 파일과 CLI 순서로 보여 준다.
- 전체 로그를 덤프하지 말고 판단을 바꾼 줄만 남긴다.
- 마지막에는 제공된 trace가 짧아 일부 질문은 관찰 불가로 남습니다. 같은 남은 경계를 사람 말로 다시 정리한다.
