# 지식 인덱스

## 재사용 가능한 개념

- soft delete는 "지우지 않는다"가 아니라 "목록과 후속 동작의 기본 경계를 바꾼다"는 의미다.
- optimistic locking은 DB 잠금보다 먼저 설명하기 좋은 충돌 감지 도구다.
- CRUD 랩도 서비스 계층이 있으면 규칙 설명이 훨씬 쉬워진다.

## 용어집

- `soft delete`: 실제 행 삭제 대신 삭제 시점을 기록해 논리적으로 숨기는 방식
- `optimistic locking`: 충돌이 드물다고 가정하고, 쓰기 시점에 버전 충돌을 감지하는 방식
- `stale update`: 오래된 version을 가진 수정 요청

## 참고 자료

- 제목: `labs/D-data-api-lab/problem/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: 새 문제 프레이밍의 데이터 범위와 성공 기준을 맞추기 위해 확인했다.
  - 배운 점: 이 랩의 핵심은 CRUD 자체보다 데이터 규칙을 드러내는 데 있다.
  - 반영 결과: 새 `00-problem-framing.md`와 `01-approach-log.md`에 반영했다.
- 제목: `labs/D-data-api-lab/fastapi/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: 현재 실행 명령과 데이터 API 범위를 active workspace 기준으로 다시 확인하기 위해 읽었다.
  - 배운 점: 이 랩은 인증 없는 상태에서도 데이터 규칙만으로 충분히 학습 가치가 있다.
  - 반영 결과: 새 `00-problem-framing.md`와 `05-development-timeline.md`에 범위와 재현 순서를 더 명확히 적었다.
