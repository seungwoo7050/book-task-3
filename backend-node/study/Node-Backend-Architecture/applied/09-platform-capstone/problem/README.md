# Problem

## canonical problem statement

여러 단계에서 학습한 규약과 기능을 단일 NestJS 서비스로 다시 조합해 구조 일관성을 검증하는 것이 canonical problem이다.

## 성공 기준

- auth, books, events, persistence, 운영성 규약이 한 서비스 안에서 함께 동작할 것
- native SQLite 복구 절차를 포함해 재현 가능한 검증 명령을 남길 것
- 단계별 학습 산출물이 capstone 안에서 어떻게 연결되는지 설명할 것

## 제공 자료

- capstone 문제 설명
- NestJS 워크스페이스
- 개념 문서
- 학습 로그
- SQLite 복구 가이드

## 제외 범위

- Postgres, Redis, Docker Compose를 포함한 제출용 패키징
- queue/worker 분리와 별도 비동기 프로세스 운영
- 실제 클라우드 배포와 운영 자동화

## 이 문제를 푸는 공개 답안

- [NestJS capstone 레인](../nestjs/README.md)
