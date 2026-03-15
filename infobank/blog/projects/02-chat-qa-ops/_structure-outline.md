# 02 챗봇 상담 품질 관리 Structure Outline

이 outline의 목적은 독자가 이 프로젝트를 "챗봇 앱"이 아니라 "quality operations system"으로 읽게 만드는 것이다. 그래서 문서 구조를 `평가 파이프라인 -> 증빙 -> 운영 표면` 순서로 고정했다.

## 문서 구성 의도

- `00-series-map.md`
  - 프로젝트를 어떤 질문으로 읽을지, 그리고 historical proof와 current rerun을 왜 분리해야 하는지 먼저 잡는다.
- `10-first-qa-evaluation-loop.md`
  - Rule -> Evidence -> Judge 순서와 trace 저장 구조를 설명한다.
- `20-regression-hardening-and-proof.md`
  - compare/dashboard/proof artifact가 improvement story를 어떻게 만들고, current snapshot 재실행과는 어디서 갈라지는지 설명한다.
- `30-self-hosted-review-ops.md`
  - 같은 평가 grammar가 auth, dataset, KB bundle, async job, selected review UI를 가진 운영 surface로 이동하는 과정을 설명한다.

## 문체 기준

- `10`은 "왜 이 순서의 파이프라인이 필요한가"에 답해야 한다.
- `20`은 "proof artifact가 무엇을 증명하고, 현재 재실행은 무엇을 보여 주는가"를 분리해서 다뤄야 한다.
- `30`은 "새 evaluator가 아니라 운영 단위가 어떻게 추가됐는가"를 보여 줘야 한다.

## 이번 재작성에서 특히 지킨 점

- `make compare`와 CLI 시그니처 불일치를 현재 seam으로 남긴다.
- docs/demo improvement artifact를 그대로 현재 재현 결과처럼 포장하지 않는다.
- `v3` 테스트 통과와 비차단 경고를 함께 남겨, 운영 snapshot의 현재 상태를 과장하지 않는다.
