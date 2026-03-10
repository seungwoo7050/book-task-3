# 01-quality-rubric-and-score-contract 지식 인덱스

## 핵심 개념

- weighted rubric 설계
- critical override와 grade band의 분리
- judge 출력과 final score merge 계약

## 참고 경로

## 품질 루브릭 계약
- 제목: Quality Rubric Contract
- 경로: chat-qa-ops/01-quality-rubric-and-score-contract/python/src/stage01/rubric.py
- 확인 날짜: 2026-03-07
- 참고 이유: score 계산 규칙을 가장 작은 형태로 고정하기 위해 확인했다.
- 배운 점: scoring vocabulary를 먼저 얼려두면 후속 실험이 숫자 비교로 귀결된다.
- 현재 프로젝트에 준 영향: v1/v2 compare도 동일한 score axes를 공유하게 했다.
