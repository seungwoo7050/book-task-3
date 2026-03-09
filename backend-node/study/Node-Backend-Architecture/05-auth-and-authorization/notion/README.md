# 05-auth-and-authorization — Notion 문서 가이드

## 이 폴더의 목적

이 `notion/` 폴더는 프로젝트를 Notion으로 옮길 때 그대로 사용할 수 있는 문서 세트다.
JWT 인증과 RBAC 인가를 Express와 NestJS에서 각각 구현한 과정을 담고 있다.

## 문서 목록과 읽는 순서

| 순서 | 문서 | 설명 |
|------|------|------|
| 1 | [essay.md](essay.md) | 프로젝트 에세이 — 인증과 인가를 왜 이 시점에 붙이고 어떤 선택을 했는지 서사적으로 설명한다 |
| 2 | [timeline.md](timeline.md) | 개발 타임라인 — bcrypt, JWT, Passport 등을 도입하며 거친 전체 과정을 순서대로 기록한다 |

## 누가 언제 읽으면 좋은가

- **JWT 기반 인증 흐름을 이해하고 싶은 사람**: `essay.md`를 읽으면 된다
- **Express 미들웨어 체인과 NestJS Guard의 차이를 알고 싶은 사람**: `essay.md`의 비교 섹션을 읽으면 된다
- **처음부터 재현하고 싶은 사람**: `timeline.md`를 따라가면 된다
