# 문제 프레이밍

> 프로젝트: NP-완전성 실습
> 아래 내용은 `notion-archive/00-problem-framing.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 첫인상

CLRS Ch 34 NP-완전성. 직접 풀지 않고, 주어진 인증서(certificate)가 올바른지 다항 시간에 검증하는 verifier 구현.

## 프로젝트 구조

`VC` 모드: Vertex Cover 인증서 검증. `3SAT` 모드: 3-SAT 인증서 검증.

## 왜 이 프로젝트인가

NP 문제의 핵심은 "검증은 쉽다". 이를 직접 코드로 체험.

## 지금 이 프로젝트에서 먼저 고정할 것

- `NP-완전성 실습`에서 실제로 확인하려는 학습 목표는 `NP-완전성 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`이다.
- 문제를 읽을 때는 "정답을 맞힌다"보다 어떤 상태와 규칙을 끝까지 유지해야 하는지를 먼저 적어 두는 편이 좋다.
- CLRS Ch 34의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.
- 학습자 입장에서는 `05-development-timeline.md`를 같이 열어 두면 실제 재현 순서와 문제 해석이 어떻게 맞물리는지 더 잘 보인다.

## 시작 전 성공 기준

- `problem/README.md`의 입력 계약을 내 말로 다시 쓸 수 있는가?
- `python/src/solution.py`를 읽기 전에 어떤 자료구조나 상태 정의가 필요할지 예측했는가?
- `make -C problem test`를 돌렸을 때 어떤 fixture가 왜 필요한지 설명할 수 있는가?

## 같이 다시 볼 문서

- [`certificate-verifier-concept.md`](../docs/concepts/certificate-verifier-concept.md)
- [`edge-cases.md`](../docs/concepts/edge-cases.md)
- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../0x17-number-theory-lab/README.md`](../../0x17-number-theory-lab/README.md) (정수론 실습)
