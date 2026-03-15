# 00-source-brief 문제지

## 왜 중요한가

이 문서는 runtime이 분리된 구현을 한 장에서 섞어 읽지 않도록 경계를 세우는 umbrella 문제지다.

## 목표

하나의 개념을 여러 runtime으로 옮긴 구현 중 어떤 문서를 먼저 읽어야 할지 바로 결정한다.

## 시작 위치

- `python`: [`00-source-brief-python`](00-source-brief-python.md)
- runtime leaf 문제지에서 실제 source, test, fixture를 다시 확인한다.

## starter code / 입력 계약

- 실제 starter code와 입력 계약은 각 runtime 문제지에서 직접 확인한다.

## 핵심 요구사항

- 필요한 runtime을 하나 고른 뒤 그 문서만 기준으로 구현을 시작한다.
- runtime 사이 구현을 섞어 읽지 않는다.

## 제외 범위

- 이 umbrella 문서는 구현 해설을 대신하지 않는다.
- 검증 명령은 runtime leaf 문서에서 사용한다.

## 성공 체크리스트

- 어떤 runtime 문서를 읽어야 하는지 즉시 결정할 수 있다.
- 선택한 runtime 문서만으로 구현을 시작할 수 있다.

## 검증 방법

```bash
cd /Users/woopinbell/work/book-task-3/infobank/projects/02-chat-qa-ops/stages/00-source-brief/python && PYTHONPATH=src python3 -m pytest
```

- umbrella 문서는 첫 번째 runtime leaf의 검증 명령을 대표값으로 보여 준다.
- 실제 구현 검증은 선택한 runtime leaf 문제지에서 다시 확인한다.

## 스포일러 경계

정답 코드, 공식 구현 진입점, 해설은 [`00-source-brief_answer.md`](00-source-brief_answer.md)에서 확인한다.
