# 03 차별화 포인트와 노출 설계 문서 안내

한국어 추천 문구와 differentiation point를 설계해 사용자가 추천 이유를 바로 이해하도록 만드는 단계다.

## 오래 남길 개념

- 추천 결과를 단순 점수가 아니라 설명 가능한 문장으로 바꾸는 법
- 한국어 시장 맥락에 맞는 노출 필드와 reason template 설계
- 운영자 화면과 사용자-facing 문구를 연결하는 방식

## 같이 볼 파일

- `../README.md`
- `08-capstone-submission/v0-initial-demo/shared/src/catalog.ts`
- `08-capstone-submission/v0-initial-demo/node/src/services/recommendation-service.ts`
- `08-capstone-submission/v0-initial-demo/react/components/mcp-dashboard.tsx`

## 이 단계를 문서로 남기는 이유

- 이 stage는 capstone 구현을 읽기 위한 기준 문장과 개념 인덱스를 맡는다.
- 빠르게 현재 상태를 파악할 수 있어야 하므로 장문의 시행착오는 `notion/`으로 분리한다.
- 이 단계는 ranking 수치 자체보다, 추천 이유를 어떻게 표현할지를 다룬다.

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
