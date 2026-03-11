# 00 문제 정의와 기준 문서

## 이 stage의 문제

MCP 추천 최적화 트랙에서 무엇을 만들고 어떤 기준으로 좋은 추천을 판단할지 먼저 고정한다.

## 입력/제약

- 입력: `docs/curriculum/project-selection-rationale.md`, `docs/curriculum/reference-spine.md`, capstone baseline 코드
- 제약: 별도 runtime을 만들지 않고, 이후 버전이 따라야 할 읽기 기준만 남긴다.

## 이 stage의 답

- reference spine과 capstone baseline 연결 경로를 문서로 고정한다.
- 추천 시스템 설명을 기능 목록이 아니라 커리큘럼 기준선으로 읽게 만든다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/catalog.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/eval.ts`

## 검증 명령

- 별도 stage-local 실행 명령은 없다.
- `problem/README.md`, `docs/README.md`, capstone `v0` 코드 포인터가 서로 같은 질문을 가리키는지 확인한다.

## 현재 한계

- 실제 동작 코드는 없고 navigation contract만 제공한다.
- 추천 품질 계약의 구체 구현은 이후 stage와 capstone에 있다.
