# 레포 문서 안내

이 폴더는 레포 전체를 이해하기 위한 공통 문서를 모아 둔 곳이다. 처음 들어온 사람이 "무슨 과제를, 왜 이렇게 나눴고, 어느 순서로 읽어야 하는가"를 빠르게 파악하도록 돕는 것이 목적이다.

## 이 폴더에서 읽을 문서

- `project-selection-rationale.md`: 왜 이 레포를 "과제별 한 번에 완성"이 아니라 단계형 트랙으로 다시 설계했는지 설명한다.
- `curriculum-map.md`: 각 트랙의 `00 -> 08` 단계가 무엇을 배우게 하는지 한눈에 보여 준다.
- `reference-spine.md`: 각 트랙이 어떤 공식 문서와 기준 교재를 뼈대로 삼는지 정리한다.
- `legacy-intent-audit.md`: 과제 설명의 원래 의도와 현재 레포 구조가 어디서 만나고 어디서 달라졌는지 정리한다.

## 문서 운영 원칙

- 핵심 안내 문서는 한글 우선으로 유지한다.
- 구현 세부사항보다 먼저 읽는 순서, 현재 상태, 검증 경로를 알려 준다.
- 경로, 버전, 실행 명령은 실제 파일 기준으로 적고 추측하지 않는다.
- `README.md`, `problem/`, `docs/`는 빠른 진입용 공개 안내서로, `notion/`은 판단 과정과 회고를 담는 공개 백업 문서로 역할을 나눈다.

## notion 정책

- `notion/`은 숨김 메모 폴더가 아니라 레포에 포함되는 공개 백업 문서다.
- 새 기준으로 다시 쓰고 싶을 때는 기존 `notion/`을 삭제하지 않고 `notion-archive/`로 옮겨 보존한다.
- 새 `notion/`은 `README.md`, `00-problem-framing.md`, `01-approach-log.md`, `02-debug-log.md`, `03-retrospective.md`, `04-knowledge-index.md`, `05-development-timeline.md`를 기본 세트로 사용한다.
- `05-development-timeline.md`는 단순 작업 일지가 아니라, 학습자가 같은 결과를 다시 재현할 수 있게 읽는 순서와 실행 순서를 남기는 핵심 문서다.

## 추천 읽기 순서

1. `project-selection-rationale.md`
2. `curriculum-map.md`
3. `reference-spine.md`
4. 각 트랙의 `README.md`
5. 각 트랙의 `08-capstone-submission/README.md`

## 학생용 추천 경로

- 과제의 큰 그림이 먼저 필요하면 `project-selection-rationale.md`와 `curriculum-map.md`를 읽는다.
- 바로 결과물이 보고 싶으면 각 트랙의 `08-capstone-submission/README.md`와 상위 `notion/05-development-timeline.md`를 같이 읽는다.
- 내 공개 포트폴리오 레포를 설계하려면 `README.md`, `problem/`, `docs/`, `notion/05-development-timeline.md`가 각각 어떤 역할을 맡는지 비교해 본다.

## 포트폴리오로 옮길 최소 세트

- `README.md`: 처음 방문한 사람이 현재 상태와 실행 경로를 이해하게 만드는 공개 입구
- `problem/README.md`: 문제와 고정 범위를 분리해 주는 계약 문서
- `docs/README.md`: 오래 남길 개념, 증빙, 검증 기준을 모아 둔 stable index
- `notion/05-development-timeline.md`: 재현 가능한 읽기 순서와 실행 순서를 남기는 핵심 노트
- `notion-archive/`: 예전 사고 흐름과 장문 시행착오를 지우지 않고 보존하는 백업

## 지금 이 레포에서 기억할 점

- 활성 트랙은 `mcp-recommendation-demo/`와 `chat-qa-ops/` 두 개다.
- 현재 구조에는 별도 `legacy/` 디렉터리가 없다. 나중에 추가되더라도 읽기 전용 참조 이상으로 취급하지 않는다.
