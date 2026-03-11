# 01 추천 품질 기준과 평가 계약

## 이 stage의 문제

좋은 추천을 어떤 rubric과 offline eval contract로 판정할지 먼저 고정한다.

## 입력/제약

- 입력: 추천 품질 축, acceptance threshold, offline eval fixture
- 제약: runtime 추천 로직보다 먼저 평가 vocabulary를 안정화한다.

## 이 stage의 답

- 추천 품질 rubric과 acceptance threshold를 문서 기준으로 분리한다.
- offline eval contract를 shared schema와 service 구조로 연결할 기준점을 만든다.

## capstone 연결 증거

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/contracts.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/eval.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/node/src/services/eval-service.ts`

## 검증 명령

- 별도 stage-local 실행 명령은 없다.
- capstone `v0` contract와 eval service가 `problem/README.md`의 완료 기준을 충족하는지 확인한다.

## 현재 한계

- 점수 계약을 실제 운영 로그와 묶는 일은 아직 다루지 않는다.
- 비교 실험과 release gate는 후속 stage에 남겨 둔다.
