# 00 문제 정의와 방향 고정 문서 안내

legacy 감사 결과와 최종 capstone 방향을 실행 가능한 source brief contract로 고정하는 단계다.

## 오래 남길 개념

- 문서 중심 기획을 코드 계약으로 고정하는 방법
- baseline snapshot과 curriculum rationale의 분리
- reference spine을 stable navigation으로 유지하는 원칙

## capstone에서 이어지는 이유

- `08/v0`를 기준점으로 삼는 이유를 stage 단위에서 먼저 고정한다.
- 이후 모든 README와 verification 문서는 이 source brief를 따라야 한다.

## 현재 확인 가능한 범위

- 실제 구현: reference source manifest, project selection rationale snapshot
- 아직 남은 범위: capstone runtime 없음

## 검증 메모

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

- 테스트는 topic, baseline version, primary stack, reference spine 길이를 고정한다.
- runtime을 검증하는 단계는 아니므로 build보다 contract drift 방지가 핵심이다.

## 노트 운영 원칙

- tracked 문서는 빠른 현재 상태와 개념 인덱스를 맡는다.
- `notion/`은 판단 과정, 실패 기록, 회고를 담는 공개 백업 문서다.
- 새 버전으로 다시 정리할 때는 기존 노트를 `notion-archive/`로 옮겨 보존한다.

## 학생이 이 문서 묶음에서 바로 가져갈 것

- `README.md`, `problem/README.md`, `docs/README.md`, `notion/05-development-timeline.md`를 서로 다른 공개 역할로 나누는 방식
- 현재 단계의 검증 명령과 acceptance 기준을 짧은 공개 문서로 남기는 방식
- 장문 시행착오는 `notion/`으로 보내고, 오래 남길 개념과 증빙만 tracked docs에 남기는 방식

## notion과 05 타임라인을 읽는 법

- 빠른 현재 상태는 tracked docs에서 먼저 확인한다.
- 같은 결과를 다시 재현하려면 `../notion/05-development-timeline.md`를 따라 읽고 실행한다.
- 새 기준으로 다시 쓰고 싶다면 기존 `notion/`을 `../notion-archive/`로 옮긴 뒤 새 `notion/`을 만든다.
