# 04-claim-and-evidence-pipeline 지식 인덱스

## 핵심 개념

- claim extraction
- retrieval trace
- verdict trace와 evidence document linkage

## 참고 경로

## 근거 검증 trace 구조
- 제목: Evidence Verifier Trace Shape
- 경로: projects/02-chat-qa-ops/capstone/v1-regression-hardening/python/backend/src/evaluator/evidence_verifier.py
- 확인 날짜: 2026-03-07
- 참고 이유: capstone에서 어떤 trace 항목이 실제로 필요한지 확인하기 위해 읽었다.
- 배운 점: retrieval query, returned docs, verdict, evidence ids를 한 덩어리로 봐야 groundedness를 설명할 수 있다.
- 현재 프로젝트에 준 영향: stage04는 retrieval trace와 verdict trace를 최소 schema로 유지했다.
