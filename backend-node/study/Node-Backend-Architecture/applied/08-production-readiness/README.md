# 08-production-readiness

- 그룹: `Applied`
- 상태: `verified`
- 공개 답안 레인: `nestjs/`
- 성격: 신규 설계

## 한 줄 문제

애플리케이션 코드 바깥의 Docker, config, health, logging, CI, cache, queue, rate limiting을 학습용 서비스에 붙이는 운영성 문제다.

## 성공 기준

- config, health/readiness, logging 같은 운영 규약을 서비스 코드와 함께 설명할 수 있다.
- Dockerfile과 CI 예시를 로컬 재현 명령과 연결할 수 있다.
- cache, queue, rate limiting을 왜 여기서 맛보기로 넣는지 설명할 수 있다.

## 내가 만든 답

- `nestjs/` 단일 레인으로 production-readiness 체크리스트를 재현하는 예제 서비스를 만들었다.
- health/readiness endpoint, structured logging, Dockerfile, CI 초안을 묶어 운영성 관점을 드러냈다.
- 이후 capstone이 기능을 통합할 수 있도록 공통 운영 규약을 먼저 마련했다.

## 제공 자료

- `problem/README.md`
- `nestjs/`
- `docs/`
- `notion/`

## 실행과 검증

### NestJS 운영성 레인
- 작업 디렉터리: `nestjs/`
- install: `pnpm install`
- verify: `pnpm run build && pnpm run test && pnpm run test:e2e`
- run: `pnpm run start`

## 왜 다음 단계로 이어지는가

- `09-platform-capstone`에서 03~08의 규약을 단일 NestJS 서비스로 통합한다.
- canonical problem statement는 [problem/README.md](problem/README.md)에서, 구현별 실행 메모는 [nestjs/README.md](nestjs/README.md)에서 확인한다.
