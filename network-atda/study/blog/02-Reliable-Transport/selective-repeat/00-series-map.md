# Selective Repeat series map

이 프로젝트를 읽을 때 붙들 질문은 하나다. 개별 ACK과 수신 버퍼링이 Go-Back-N 다음 단계에서 어떤 차이를 만드는가?

## 무엇을 근거로 복원했는가

- 프로젝트 README: `study/02-Reliable-Transport/selective-repeat/README.md`
- 문제 문서와 실행 표면: `study/02-Reliable-Transport/selective-repeat/problem/README.md`, `study/02-Reliable-Transport/selective-repeat/problem/Makefile`
- 핵심 구현과 테스트: `study/02-Reliable-Transport/selective-repeat/python/src/selective_repeat.py`, `study/02-Reliable-Transport/selective-repeat/python/tests/test_selective_repeat.py`
- 정식 검증 출력: `make -C study/02-Reliable-Transport/selective-repeat/problem test`

## 어떤 순서로 읽으면 되는가

1. `problem/README.md`로 문제 조건과 성공 기준을 확인한다.
2. 이 문서에서 어떤 입력을 근거로 썼는지 먼저 본다.
3. `01-evidence-ledger.md`로 세 단계 흐름을 짧게 파악한다.
4. `10-development-timeline.md`에서 코드나 trace, CLI를 따라간다.

## 이번 리라이트에서 의도적으로 제외한 입력

- 현재 `study/blog/**`의 이전 본문
- `notion/`, `notion-archive/` 아래의 서술형 메모

## 짧은 판정 메모

- 독립 프로젝트로 본 이유: `Selective Repeat`는 자기 README와 정식 검증 명령으로 범위를 독립적으로 설명할 수 있다.
- 보관본 위치: `study/blog/_legacy`
- 이번 글의 중심 답: Go-Back-N`의 한계를 보강하기 위해 추가한 선택 재전송 프로젝트입니다.
