# 07 운영 대시보드와 리뷰 콘솔 문서 안내

overview, failures, session review, eval runner, version compare를 보여주는 API와 React UI를 stage 단위로 집중 분리한 단계다.

## 오래 남길 개념

- snapshot API
- dashboard information architecture
- session review trace surfacing
- baseline/candidate version compare

## capstone에서 이어지는 이유

- v1 dashboard slice를 그대로 복제해 stage07에서 UI contract를 독립 학습할 수 있게 했다.
- v2 improvement proof가 결국 어떤 화면과 API에서 읽혀야 하는지 보여준다.

## 현재 확인 가능한 범위

- 실제 구현: FastAPI snapshot endpoints, React dashboard pages and mocked tests
- 아직 남은 범위: 실제 DB persistence 없음

## 검증 메모

- `cd python && UV_PYTHON=python3.12 uv run pytest -q`
- `cd react && pnpm test --run`

- Python pack은 snapshot endpoint contract를 테스트한다.
- React pack은 mocked Vitest로 overview, failures, session review, eval runner, compare UI를 검증한다.

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
