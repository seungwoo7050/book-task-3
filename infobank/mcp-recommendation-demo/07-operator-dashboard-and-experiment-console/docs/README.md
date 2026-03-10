# 07 운영자 대시보드와 실험 콘솔 문서 안내

catalog, experiment, release candidate를 한 화면에서 다루는 운영 콘솔을 정리해 추천 시스템의 운영 면을 보여 주는 단계다.

## 오래 남길 개념

- 운영자 화면에서 무엇을 먼저 보여 줘야 하는지
- catalog 관리, 실험 관리, release candidate 관리를 한 콘솔로 묶는 법
- 실험 결과와 운영 작업을 같은 정보 구조에서 다루는 방식

## 같이 볼 파일

- `../README.md`
- `08-capstone-submission/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
- `08-capstone-submission/v2-submission-polish/react/components/mcp-dashboard.tsx`
- `08-capstone-submission/v2-submission-polish/tests/e2e/recommendation.spec.ts`

## 이 단계를 문서로 남기는 이유

- 이 stage는 capstone 구현을 읽기 위한 기준 문장과 개념 인덱스를 맡는다.
- 빠르게 현재 상태를 파악할 수 있어야 하므로 장문의 시행착오는 `notion/`으로 분리한다.
- 이 단계는 UI 컴포넌트 목록보다, 운영자가 무엇을 보고 어떤 결정을 내리는지에 초점을 둔다.

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
