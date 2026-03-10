# 00 문제 정의와 기준 문서 문서 안내

MCP 추천 최적화 트랙에서 무엇을 만들고 어떤 기준으로 좋은 추천을 판단할지 먼저 고정하는 단계다.

## 오래 남길 개념

- reference spine을 먼저 정해 읽어야 할 문서 수를 줄이는 법
- capstone 코드를 보기 전에 문제 정의와 평가 기준을 먼저 고정하는 법
- 학습용 레포에서 설계 문서와 실제 구현 경로를 연결하는 인덱스 작성법

## 같이 볼 파일

- `../README.md`
- `08-capstone-submission/v0-initial-demo/shared/src/catalog.ts`
- `08-capstone-submission/v0-initial-demo/shared/src/eval.ts`
- `../../docs/reference-spine.md`
- `../../docs/project-selection-rationale.md`

## 이 단계를 문서로 남기는 이유

- 이 stage는 capstone 구현을 읽기 위한 기준 문장과 개념 인덱스를 맡는다.
- 빠르게 현재 상태를 파악할 수 있어야 하므로 장문의 시행착오는 `notion/`으로 분리한다.
- 이 단계는 문서 단계다. 별도 구현 디렉터리를 만들기보다, 어떤 코드를 읽어야 하는지 정확히 가리키는 것이 더 중요하다.

## notion과의 관계

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
