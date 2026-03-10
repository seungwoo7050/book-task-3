# 지식 인덱스

## 재사용 가능한 개념

- 비동기 설계의 핵심은 broker 선택보다 handoff boundary다.
- eager mode는 "동기 실행"일 뿐, 설정 문제를 사라지게 하지 않는다.
- 상태 전이와 시도 횟수 같은 부수 효과는 같은 규칙 안에서 관리해야 한다.

## 용어집

- `outbox`: 작업 전달 전에 DB에 남겨 두는 중간 저장소
- `idempotency key`: 같은 요청을 여러 번 보내도 한 번처럼 취급하기 위한 키
- `eager mode`: worker를 따로 띄우지 않고 현재 프로세스에서 작업을 즉시 실행하는 테스트 모드

## 참고 자료

- 제목: `labs/E-async-jobs-lab/problem/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: 새 문제 프레이밍에서 비동기 경계의 성공 기준을 고정하기 위해 확인했다.
  - 배운 점: 이 랩은 작업 실행 자체보다 안전한 handoff를 설명하는 데 초점이 있다.
  - 반영 결과: 새 `00-problem-framing.md`와 `01-approach-log.md`에 반영했다.
- 제목: `labs/E-async-jobs-lab/fastapi/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: API와 worker를 함께 띄우는 현재 워크스페이스 구조를 다시 확인하기 위해 읽었다.
  - 배운 점: 비동기 랩은 실행 문서가 handoff boundary 설명의 일부가 된다.
  - 반영 결과: 새 `05-development-timeline.md`와 `00-problem-framing.md`에 API/worker 경계를 더 선명하게 적었다.
