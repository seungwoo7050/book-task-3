# Traceroute series map

이 프로젝트를 읽을 때 붙들 질문은 하나다. UDP probe와 ICMP 응답을 엮어 hop 단위 경로를 어떻게 복원했는가?

## 무엇을 근거로 복원했는가

- 프로젝트 README: `study/04-Network-Diagnostics-and-Routing/traceroute/README.md`
- 문제 문서와 실행 표면: `study/04-Network-Diagnostics-and-Routing/traceroute/problem/README.md`, `study/04-Network-Diagnostics-and-Routing/traceroute/problem/Makefile`
- 핵심 구현과 테스트: `study/04-Network-Diagnostics-and-Routing/traceroute/python/src/traceroute.py`, `study/04-Network-Diagnostics-and-Routing/traceroute/python/tests/test_traceroute.py`
- 정식 검증 출력: `make -C study/04-Network-Diagnostics-and-Routing/traceroute/problem test`

## 어떤 순서로 읽으면 되는가

1. `problem/README.md`로 문제 조건과 성공 기준을 확인한다.
2. 이 문서에서 어떤 입력을 근거로 썼는지 먼저 본다.
3. `01-evidence-ledger.md`로 세 단계 흐름을 짧게 파악한다.
4. `10-development-timeline.md`에서 코드나 trace, CLI를 따라간다.

## 이번 리라이트에서 의도적으로 제외한 입력

- 현재 `study/blog/**`의 이전 본문
- `notion/`, `notion-archive/` 아래의 서술형 메모

## 짧은 판정 메모

- 독립 프로젝트로 본 이유: `Traceroute`는 자기 README와 정식 검증 명령으로 범위를 독립적으로 설명할 수 있다.
- 보관본 위치: `study/blog/_legacy`
- 이번 글의 중심 답: TTL 증가와 `ICMP Time Exceeded`를 이용해 hop-by-hop 경로를 드러내는 bridge 프로젝트입니다.
