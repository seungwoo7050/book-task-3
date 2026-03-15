# Problem

## canonical problem statement

학습용 capstone을 채용 검토자가 바로 읽고 실행할 수 있는 shippable backend service 형태로 다시 패키징하는 것이 canonical problem이다.

## 성공 기준

- Postgres migration과 Redis 의존성을 포함한 로컬 실행 흐름을 제공할 것
- Swagger, health endpoint, auth/books API를 한 서비스 표면으로 설명할 것
- 학습용 capstone과 제출용 서비스의 차이를 문서화할 것

## canonical verification 시작 위치

- 실행과 검증 진입점은 [../nestjs/README.md](../nestjs/README.md)다.

## 제공 자료

- 문제 설명
- NestJS 워크스페이스
- Docker Compose
- 운영/발표 문서
- 학습 로그

## 제외 범위

- 별도 queue/worker 프로세스와 이벤트 브로커 운영
- MSA 분리와 서비스 간 네트워크 통신
- 실제 클라우드 배포와 외부 SaaS 연동

## 이 문제를 푸는 공개 답안

- [NestJS 포트폴리오 레인](../nestjs/README.md)
