# 05 로그, 지표, 피드백 루프 문서 안내

usage event, feedback record, experiment metadata를 DB와 API로 연결해 추천 품질 개선의 운영 루프를 설명하는 단계다.

## 오래 남길 개념

- 추천 서비스에서 어떤 로그와 피드백을 남겨야 하는지
- 실험 메타데이터를 운영자 콘솔과 연결하는 법
- 사용 로그를 다음 실험 설계와 품질 개선으로 잇는 방식

## 같이 볼 파일

- `../README.md`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/db/schema.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/repositories/catalog-repository.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/app.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`

## 이 단계를 문서로 남기는 이유

- 이 stage는 capstone 구현을 읽기 위한 기준 문장과 개념 인덱스를 맡는다.
- 빠르게 현재 상태를 파악할 수 있어야 하므로 장문의 시행착오는 `notion/`으로 분리한다.
- 이 단계는 추천 품질을 '사용 이후'까지 추적하는 구조를 다룬다.

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
