# 01 MCP 추천 최적화 Structure Outline

이 outline은 이 시리즈를 왜 지금의 네 문서 구조로 나눴는지 설명한다. 목표는 기능 목록을 나열하는 것이 아니라, 독자가 "추천 시스템이 어떻게 단단해졌는가"를 자연스러운 순서로 따라가게 만드는 것이다.

## 문서 구성 의도

- `00-series-map.md`  
  이 프로젝트를 어떤 질문으로 읽어야 하는지 먼저 정리한다. 독립 프로젝트로 본 이유, 사용한 근거, 전체 챕터 구성을 여기서 잡는다.
- `10-catalog-contracts-and-first-ranking-loop.md`  
  추천 시스템의 출발점이 ranking 자체가 아니라 catalog 계약이라는 점을 보여 준다. baseline scoring, 한국어 explanation, candidate rerank까지 여기서 묶는다.
- `20-ranking-proof-and-release-gates.md`  
  추천 결과가 compare, compatibility, release gate, artifact export로 이어지는 과정을 보여 준다. 이 시점부터 프로젝트는 단순 추천 데모가 아니라 release 판단 도구처럼 읽히기 시작한다.
- `30-self-hosted-operator-surface.md`  
  이미 만든 proof pipeline이 `v3`에서 RBAC, async jobs, polling UI를 가진 운영 표면으로 어떻게 바뀌는지 설명한다.

## 문체 기준

- `10`은 "왜 metadata 계약부터 만들었는가"라는 질문에 답한다.
- `20`은 "추천 결과를 어떻게 제출 가능한 proof로 바꿨는가"에 답한다.
- `30`은 "같은 proof를 어떻게 self-hosted 운영 흐름으로 옮겼는가"에 답한다.

좋은 점은 세 문서가 서로 다른 기능을 설명하는 글이 아니라, 하나의 시스템이 다른 수준의 책임을 차례대로 떠안는 과정을 나눠 보여 준다는 데 있다.
