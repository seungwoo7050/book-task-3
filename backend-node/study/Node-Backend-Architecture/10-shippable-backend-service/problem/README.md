# Problem

## 목표

`09-platform-capstone`에서 통합한 auth + books + events 서비스를
채용 제출이 가능한 shippable backend 형태로 강화한다.

## 요구사항

- 공개 API 계약은 유지한다.
  - `POST /auth/register`
  - `POST /auth/login`
  - `/books` CRUD
- 새 운영 인터페이스를 추가한다.
  - `GET /health/live`
  - `GET /health/ready`
  - `GET /docs`
- DB는 SQLite가 아니라 Postgres migration 기반이어야 한다.
- seed script로 admin 계정과 demo books를 만들 수 있어야 한다.
- Redis는 public books 조회 캐시와 로그인 실패 throttling에만 사용한다.
- Docker Compose와 `.env.example`만으로 로컬 실행 경로를 재현할 수 있어야 한다.

## 제공 자료

- `code/nestjs/`: legacy capstone starter의 최소 골격
- `script/nestjs/Makefile`: 초기 참고 스크립트

## 정답 공개 정책

이 프로젝트는 정답집이 아니라 학습/포트폴리오용 보강 과제다.
문제와 구현을 분리해 두되, README와 docs에서는 왜 이런 구조가 채용 경쟁력과 연결되는지까지 설명한다.
