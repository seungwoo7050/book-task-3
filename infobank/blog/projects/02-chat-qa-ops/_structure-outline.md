# 02 챗봇 상담 품질 관리 Structure Outline

이 outline은 이 시리즈를 왜 지금의 네 문서 구조로 나눴는지 설명한다. 목표는 기능 목록을 나열하는 것이 아니라, 독자가 "상담 품질 평가가 어떻게 운영 가능한 형태로 자랐는가"를 자연스러운 순서로 따라가게 만드는 것이다.

## 문서 구성 의도

- `00-series-map.md`  
  이 프로젝트를 어떤 질문으로 읽어야 하는지 먼저 정리한다. 독립 프로젝트로 본 이유, 사용한 근거, 전체 챕터 구성을 여기서 잡는다.
- `10-first-qa-evaluation-loop.md`  
  rule, evidence, judge, scoring이 왜 이 순서로 묶였는지 보여 준다. CLI가 왜 먼저 중요한 운영 출구가 되었는지도 여기서 설명한다.
- `20-regression-hardening-and-proof.md`  
  golden-set compare, dashboard version compare, smoke-postgres, proof artifact가 어떻게 같은 증빙 흐름을 이루는지 보여 준다.
- `30-self-hosted-review-ops.md`  
  이미 만든 proof surface가 `v3`에서 login, dataset import, async job, selected-job review UI를 가진 운영 흐름으로 어떻게 확장되는지 설명한다.

## 문체 기준

- `10`은 "품질 평가를 어떻게 설명 가능한 파이프라인으로 만들었는가"에 답한다.
- `20`은 "개선 수치를 어떻게 proof로 닫았는가"에 답한다.
- `30`은 "같은 평가 체계를 어떻게 self-hosted 운영 흐름으로 옮겼는가"에 답한다.

좋은 점은 세 문서가 서로 다른 기능을 따로 소개하는 글이 아니라, 하나의 품질 관리 시스템이 더 넓은 책임을 차례대로 떠안는 과정을 보여 준다는 데 있다.
