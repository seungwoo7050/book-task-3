# 02 도메인 픽스처와 리플레이 하니스 문서 안내

seeded knowledge base와 replay harness를 분리해 상담 품질 실험을 재현 가능한 입력 집합 위에서 수행하도록 만드는 단계다.

## 오래 남길 개념

- seeded KB 설계
- deterministic replay harness
- expected evidence document 확인 방식

## capstone에서 이어지는 이유

- v0의 replay harness와 seeded KB를 축소한 학습용 집중 구현본이다.
- v1/v2의 golden replay도 입력 fixture 분리가 핵심이다.

## 현재 확인 가능한 범위

- 실제 구현: seeded KB loader, deterministic replay harness
- 아직 남은 범위: database 없음

## 검증 메모

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`

- 테스트는 seeded KB 파일 집합과 첫 replay의 top-1 문서를 검증한다.
- DB나 vector store 없이도 회귀 입력 contract를 설명할 수 있어야 한다.

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
