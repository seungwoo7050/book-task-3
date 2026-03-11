# 03-rule-and-guardrail-engine 지식 인덱스

## 핵심 개념

- rule-based guardrail
- failure type taxonomy
- 한국어 상담 시나리오의 escalation 조건

## 참고 경로

## 필수 안내문과 escalation 규칙
- 제목: Mandatory Notice And Escalation Rules
- 경로: projects/02-chat-qa-ops/capstone/v0-initial-demo/python/backend/rules/mandatory_notices.yaml
- 확인 날짜: 2026-03-07
- 참고 이유: v0에 반영한 한국어 안전 규칙을 stage pack으로 축소 재현하기 위해 읽었다.
- 배운 점: mandatory notice와 escalation은 둘 다 compliance이지만 실패 원인이 달라 별도 분리가 필요했다.
- 현재 프로젝트에 준 영향: stage03에서는 escalation miss를 전용 failure code로 유지했다.
