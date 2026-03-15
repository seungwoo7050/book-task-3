# 01 MCP 추천 최적화 Structure Outline

이 outline의 목적은 기능 나열이 아니라 독자가 "이 프로젝트의 무게중심이 어디 있는가"를 놓치지 않게 만드는 것이다. 추천 품질만 붙잡고 읽으면 `v3` 확장도, release gate도, artifact export도 각자 흩어져 보인다. 그래서 문서 구조를 `계약 -> proof -> operator surface` 순서로 고정했다.

## 문서 구성 의도

- `00-series-map.md`
  - 이 프로젝트를 recommendation demo가 아니라 proof pipeline으로 읽게 만드는 출발점이다.
- `10-catalog-contracts-and-first-ranking-loop.md`
  - 왜 ranking보다 metadata contract와 explanation trace가 먼저였는지 설명한다.
- `20-ranking-proof-and-release-gates.md`
  - compare, compatibility, release gate, artifact export가 submission path를 어떻게 닫는지 설명한다.
- `30-self-hosted-operator-surface.md`
  - 같은 proof chain이 `v3`에서 queue, RBAC, polling UI를 가진 운영 표면으로 이동하는 과정을 설명한다.

## 문체 기준

- `10`은 "무엇을 추천할 수 있는가"의 계약을 세우는 이야기여야 한다.
- `20`은 "무엇을 릴리즈 가능한 후보라고 부를 수 있는가"의 판단 기준을 다뤄야 한다.
- `30`은 "누가 그 판단을 실행하고 기다릴 수 있는가"라는 운영 표면 질문을 다뤄야 한다.

## 이번 재작성에서 특히 지킨 점

- `candidateNdcg3`가 baseline과 같아도 `uplift`가 통과할 수 있다는 compare/release gate의 실제 semantics를 숨기지 않는다.
- `v3`를 완성형 제품처럼 포장하지 않고 `8 passed | 2 skipped`라는 현재 검증 상태를 그대로 남긴다.
- 기존 저품질 blog 문장을 이어 붙이지 않고, 현재 코드와 CLI가 말해 주는 chronology만 남긴다.
