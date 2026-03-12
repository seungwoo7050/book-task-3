# 09-platform-capstone

- 그룹: `Applied`
- 상태: `verified`
- 공개 답안 레인: `nestjs/`
- 성격: 초기 원본 이관 + 재검증

## 한 줄 문제

REST, pipeline, auth, persistence, events, 운영성 규약을 단일 NestJS 서비스로 통합해 구조 일관성을 검증하는 capstone 문제다.

## 성공 기준

- 03~08에서 배운 규약을 하나의 서비스 안에 자연스럽게 통합할 수 있다.
- auth, books, events, persistence를 모듈 단위로 설명할 수 있다.
- build/test/e2e 재현 흐름을 하나의 README에서 안내할 수 있다.

## 내가 만든 답

- `nestjs/` 단일 레인으로 Books 플랫폼형 capstone 서비스를 구성했다.
- 이전 단계에서 만든 규약을 억지로 바꾸지 않고 통합해 일관성을 보여 준다.
- `10-shippable-backend-service`로 가기 전에 학습용 통합판을 유지한다.

## 제공 자료

- `problem/README.md`
- `nestjs/`
- `docs/`
- `notion/`
- `../../docs/native-sqlite-recovery.md`

## 실행과 검증

### NestJS capstone 레인
- 작업 디렉터리: `nestjs/`
- install: `pnpm install && pnpm approve-builds && pnpm rebuild better-sqlite3`
- verify: `pnpm run build && pnpm run test && pnpm run test:e2e`
- run: `pnpm run start:dev`

## 왜 다음 단계로 이어지는가

- `10-shippable-backend-service`에서 채용 제출용 서비스 표면으로 다시 패키징한다.
- canonical problem statement는 [problem/README.md](problem/README.md)에서, 구현별 실행 메모는 [nestjs/README.md](nestjs/README.md)에서 확인한다.
