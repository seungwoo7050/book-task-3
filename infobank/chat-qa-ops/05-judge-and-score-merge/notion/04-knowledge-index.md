# 05-judge-and-score-merge 지식 인덱스

## 핵심 개념

- judge output schema
- heuristic scoring
- quality axes merge

## 참고 경로

## LLM judge 사용 경계
- 제목: LLM Judge Boundary
- 경로: chat-qa-ops/08-capstone-submission/v1-regression-hardening/python/backend/src/evaluator/llm_judge.py
- 확인 날짜: 2026-03-07
- 참고 이유: stage05가 무엇을 분리해서 보여줘야 하는지 확인하기 위해 읽었다.
- 배운 점: judge trace와 final score merge는 결합되지만 동일 책임은 아니다.
- 현재 프로젝트에 준 영향: stage05는 판단과 계산을 분리한 최소 함수를 유지한다.
