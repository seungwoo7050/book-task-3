# 18 Workspace SaaS API Structure

## 이 글이 답할 질문

- 채용 제출용 B2B SaaS API를 로컬에서 완결형으로 재현할 수 있어야 한다.
- 이전 과제 코드를 의존성으로 가져오지 않고 대표작 내부에서 다시 소유해 제출용 완성도를 높였다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `05-portfolio-projects/18-workspace-saas-api` 안에서 `10-bootstrap-schema-and-platform.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 0 — 프로젝트 초기화와 인프라 구성 -> Phase 1 — 의존성 설치 -> Phase 2 — 마이그레이션 스키마 설계 -> Phase 3 — platform 패키지 (횡단 관심사)
- 세션 본문: `pgx/v5, google/uuid, go-redis/v9, x/crypto` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/migrations/001_init.sql`
- 코드 앵커 2: `solution/go/internal/platform/config.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: organization이 tenant boundary이고, role은 membership에 붙는다.
- 마지막 단락: 다음 글에서는 `20-auth-and-session-rotation.md`에서 이어지는 경계를 다룬다.
