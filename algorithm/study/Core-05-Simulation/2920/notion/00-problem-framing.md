# 문제 프레이밍

> 프로젝트: 음계
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

1부터 8까지의 수가 주어지면 오름차순(ascending), 내림차순(descending), 둘 다 아니면 mixed를 출력하는 문제. 시뮬레이션 트랙의 워밍업으로, "주어진 규칙을 정확히 구현한다"는 시뮬레이션의 본질을 가장 단순한 형태로 보여준다.

## 문제 구조 파악

- 8개의 정수 (1~8의 순열)
- `1 2 3 4 5 6 7 8` → ascending
- `8 7 6 5 4 3 2 1` → descending  
- 그 외 → mixed

## 왜 이 문제를 선택했는가

Core-05의 Bronze 문제로, 시뮬레이션 카테고리를 시작하는 가벼운 연습. 14891(톱니바퀴)과 14503(로봇 청소기)의 복잡한 시뮬레이션으로 가기 전에, "규칙을 코드로 변환"하는 기본 패턴을 확인한다.

## 난이도 평가

Bronze 등급. 비교 대상이 고정된 두 배열뿐이므로 직접 비교가 가장 간결하다.

## 지금 이 프로젝트에서 먼저 고정할 것

- `음계`에서 실제로 확인하려는 학습 목표는 `복잡한 설명을 작은 상태 전이 규칙으로 나누어 구현하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`simulation-concept.md`](../docs/concepts/simulation-concept.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 다음 프로젝트: [`../../14503/README.md`](../../14503/README.md) (로봇 청소기)
