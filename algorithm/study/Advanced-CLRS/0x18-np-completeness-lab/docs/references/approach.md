# 접근 정리 — NP-완전성 실습

## 문제 계약

- `problem/README.md`와 `problem/data/`가 canonical 입력/출력 계약이다.
- `problem/Makefile`이 실행과 검증의 기준선이다.
- 이 문서는 코드 전문보다 어떤 상태와 판단 순서로 구현을 읽어야 하는지 요약한다.

## 채택 답

- `python/src/solution.py`에서 `NP-완전성 실습` 핵심 절차를 실행 가능한 입출력 실험으로 재현한다.
- 정식 검증은 `make -C study/Advanced-CLRS/0x18-np-completeness-lab/problem test`를 기준으로 둔다.
- 장문 reasoning은 `../../notion/`으로 내린다.

## 왜 이 전략인가

- 이론 중심 알고리즘을 작은 실험과 검증 가능한 입출력 문제로 재구성하는 연습
- `CLRS Ch 34`의 개념을 코드와 fixture로 다시 확인할 수 있다.
- README에는 길찾기만 남기고 세부 reasoning은 `docs/`와 `notion/`으로 분리해 공개 표면을 가볍게 유지한다.

## 복잡도

- 시간 복잡도와 공간 복잡도는 `python/src/solution.py`의 구현 기준으로 읽는다.
- 입력 상한과 경계 사례는 `problem/README.md`와 `problem/data/`를 함께 확인한다.

## 실수 포인트

- 이론 설명을 그대로 옮기고 입출력 계약을 코드에 연결하지 못하는 문제
- 경계 사례를 fixture로 고정하지 않아 재검증이 어려워지는 문제
- 개념 설명이 README와 `docs/`에 중복되어 공개 표면이 흐려지는 문제

## 코드 매핑

- Python 기본 구현: `../../python/src/solution.py`
- 빠른 검증: `make -C study/Advanced-CLRS/0x18-np-completeness-lab/problem test`
- 전체 재현 흐름: `../../notion/05-development-timeline.md`
