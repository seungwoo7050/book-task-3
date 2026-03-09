# 문제 정의 — 포트폴리오 프로젝트라는 맥락

## 왜 이 프로젝트인가

"웹 백엔드 공고에 제출할 수 있는 대표 포트폴리오용 B2B SaaS API." 이 한 문장이 프로젝트의 성격을 규정한다. 학습 프로젝트가 아니라 **입사 지원서에 링크를 걸 수 있는 수준**의 코드.

캡스톤(프로젝트 17)은 게임 스토어에 집중했지만, 이 프로젝트는 B2B SaaS — 조직(tenant), 멤버, 프로젝트, 이슈, 댓글, 알림, 대시보드. 실제 업무에서 만날 수 있는 도메인이다.

## 도메인 모델

```
Organization ─┬─ Members (owner/admin/member)
               ├─ Invitations
               ├─ Projects ─── Issues ─── Comments
               ├─ Notifications
               └─ Dashboard Summary
```

조직이 tenant boundary. 한 사용자가 여러 조직에 속할 수 있다. RBAC는 owner/admin/member 3단계.

## API Surface: 17개 엔드포인트

인증: register-owner, login, refresh, logout
프로필: me
조직: invitations (create, accept)
프로젝트/이슈: CRUD + status update + comments
알림: list notifications
대시보드: summary (Redis 캐시)
운영: healthz, readyz, metrics

## 기술 스택

- **PostgreSQL**: 주 데이터 저장소 (CockroachDB가 아닌 순수 PostgreSQL)
- **Redis**: 리프레시 토큰 세션 + 대시보드 캐시
- **JWT**: HMAC-SHA256 access token + opaque refresh token
- **Outbox + Worker**: 이슈 생성/변경 시 알림 생성 (비동기)
- **API + Worker 별도 바이너리**: `cmd/api`, `cmd/worker`

## 이전 프로젝트와의 관계

```
프로젝트 07 → JWT + bcrypt 인증 (auth 패키지)
프로젝트 09 → Redis 캐시 + 메트릭 (cache, platform)
프로젝트 14 → 멱등성 키 + 트랜잭션 (service)
프로젝트 15 → Outbox + Worker (worker)
프로젝트 17 → 통합 패턴 (service 계층 구조)
```

하지만 import하지 않고 필요한 코드를 "복사 후 재소유"한다. 독립적인 모듈로서 완결성을 가져야 포트폴리오 의미가 있다.
