# 완료 기준

## 과제 해석

2번 과제는 다음 세 축을 모두 만족해야 한다.

1. 상담 품질 정의 및 점수화 기준 수립
2. 자동화 품질 평가
3. 모니터링 품질 가시화

## 포함 범위

- 상담 도메인용 최소 KB
- 채팅 로그 또는 replay 가능한 대화 입력
- rule/guardrail 기반 deterministic 평가
- claim/evidence 기반 groundedness 평가
- LLM 또는 heuristic judge
- golden set replay
- 운영용 dashboard

## 제외 범위

- 통신사 프로덕션 챗봇 전체 구현
- 대규모 실시간 배포 인프라
- 완전한 RAG 최적화 시스템
- 보너스 구현이 core를 밀어내는 과도한 확장

## 제출 완료 기준

- 데모 한 번으로 chat -> evaluate -> dashboard 흐름을 끝까지 보여줄 수 있어야 한다.
- heuristic fallback만으로도 로컬 재현이 가능해야 한다.
- rule, evidence, judge, score, dashboard가 같은 failure taxonomy를 공유해야 한다.
