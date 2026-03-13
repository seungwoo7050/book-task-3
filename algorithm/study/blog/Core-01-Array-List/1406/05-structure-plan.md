# 에디터 Structure Plan

이 시리즈는 `에디터`를 읽는 흐름이 `문제 계약 -> 첫 구현 -> 검증과 마무리`로 자연스럽게 이어지도록 나눈 메모다. 파일 구조는 그대로 두되, 각 문서가 맡는 역할은 더 분명하게 보이도록 정리했다.

## 왜 이렇게 나눴나

- `00-series-map.md`: 트랙 질문, 한 줄 답, 검증 명령을 먼저 잡아 독자가 어디서부터 읽어야 할지 안내한다.
- `10-development-timeline.md`: `Phase 1 -> Phase 2`를 묶어 문제 계약과 첫 구현이 어떻게 이어졌는지 보여 준다.
- `20-development-timeline.md`: `Phase 3 -> Phase 4`를 묶어 fixture 검증, 실수 포인트 정리, 마지막 출력/guard 정리를 함께 마무리한다.

## 각 글에서 확인할 근거

- `00`: 프로젝트 README의 한 줄 답, 트랙 질문, verify command, 복잡도
- `10`: starter skeleton, Python setup snippet, Python core snippet, 대표 실행 CLI
- `20`: `test.sh` 기반 검증, `approach.md`의 실수 포인트, Python finish snippet, `Two-Stack Editor & Linked List — Concept & Background`

## 읽으면서 확인할 질문

- `커서를 기준으로 좌/우 스택(또는 리스트) 두 개를 유지하는 editor simulation`가 실제 코드에서는 어느 상태와 반복 순서로 드러나는가?
- `make -C study/Core-01-Array-List/1406/problem test`가 마지막에 보장해 주는 건 정확히 무엇인가?
- `Two-Stack Editor & Linked List — Concept & Background`를 붙여 읽으면 어떤 줄이 이 문제의 전환점으로 보이는가?

## 톤 메모

- 결과 요약보다 구현 순서와 판단 변화가 먼저 보이게 쓴다.
- 코드와 CLI는 설명을 보조하는 예시가 아니라, 서사를 지탱하는 근거로 다룬다.
- 개념 설명은 별도 강의처럼 떼어 두지 않고, 그 개념이 실제로 필요해진 순간에 붙여 둔다.
