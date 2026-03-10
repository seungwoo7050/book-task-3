# 지식 인덱스

## 재사용 가능한 개념

- liveness와 readiness는 서로 다른 운영 질문에 답한다.
- 느린 CI 환경을 기준으로 health check 타이밍을 잡아야 한다.
- 환경 변수 기반 설정과 `lru_cache`를 함께 쓸 때는 cache clear 전략이 필수다.

## 용어집

- `liveness`: 프로세스가 살아 있는지 확인하는 신호
- `readiness`: 의존성까지 포함해 요청 처리 준비가 되었는지 확인하는 신호
- `target shape`: 실제 구축 완료가 아니라, 어떤 형태의 배포 구성을 상정하는지 설명하는 문서

## 참고 자료

- 제목: `labs/G-ops-lab/problem/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: 운영성 랩의 성공 기준과 제외 범위를 새 문서에 맞추기 위해 확인했다.
  - 배운 점: 이 랩의 핵심은 기능 수가 아니라 운영 질문에 답하는 최소 surface다.
  - 반영 결과: 새 `00-problem-framing.md`와 `01-approach-log.md`에 반영했다.
- 제목: `labs/G-ops-lab/docs/aws-deployment.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: AWS 관련 설명을 실제 배포 완료처럼 보이지 않게 active 문서 기준으로 다시 확인하기 위해 읽었다.
  - 배운 점: 운영 문서는 기술 선택보다 검증 범위와 가정의 구분이 더 중요하다.
  - 반영 결과: 새 `00-problem-framing.md`, `01-approach-log.md`, `03-retrospective.md`에 반영했다.
