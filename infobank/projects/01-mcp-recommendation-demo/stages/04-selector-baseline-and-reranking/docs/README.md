# 04 baseline selector와 reranking 문서 안내

baseline selector를 먼저 세우고 reranker와 compare runner를 더해 추천 로직 개선을 설명 가능한 형태로 만드는 단계다.

## 오래 남길 개념

- baseline selector에서 출발해 reranker로 확장하는 법
- candidate와 baseline을 같은 입력셋에서 비교하는 실험 구조
- 추천 개선을 코드와 문서 둘 다에서 설명하는 방법

## 같이 볼 파일

- `../README.md`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/recommendation-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/rerank-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/src/services/compare-service.ts`
- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/node/tests/rerank-service.test.ts`

## 이 단계를 문서로 남기는 이유

- 이 stage는 capstone 구현을 읽기 위한 기준 문장과 개념 인덱스를 맡는다.
- 빠르게 현재 상태를 파악할 수 있어야 하므로 장문의 시행착오는 `notion/`으로 분리한다.
- 이 단계는 '더 똑똑한 추천'을 만들었다는 주장보다, 왜 그렇게 판단할 수 있는지의 근거를 정리한다.

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
