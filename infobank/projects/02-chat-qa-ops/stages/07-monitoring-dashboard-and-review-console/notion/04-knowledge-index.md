# 07-monitoring-dashboard-and-review-console 지식 인덱스

## 핵심 개념

- snapshot API
- dashboard information architecture
- session review trace surfacing
- baseline/candidate version compare

## 참고 경로

## 대시보드 compare 계약
- 제목: Dashboard Compare Contract
- 경로: projects/02-chat-qa-ops/capstone/v1-regression-hardening/react/src/pages/Overview.tsx
- 확인 날짜: 2026-03-07
- 참고 이유: 운영 콘솔이 compare delta를 어떻게 읽히게 하는지 확인하기 위해 읽었다.
- 배운 점: score delta뿐 아니라 pass/fail/critical delta와 failure breakdown이 함께 보여야 개선 효과를 설득할 수 있다.
- 현재 프로젝트에 준 영향: stage07 docs와 snapshot payload에도 compare details를 포함했다.
