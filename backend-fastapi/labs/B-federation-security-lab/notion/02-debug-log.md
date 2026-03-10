# 디버그 로그

## 실패 사례

Compose 환경으로 전환했을 때 PostgreSQL 연결이 `database does not exist`로 실패한 적이 있었다. 이어서 OAuth callback 테스트에서는 state cookie가 빠져 보이는 문제도 나왔다.

## 원인

- `POSTGRES_DB`와 애플리케이션이 기대하는 `DATABASE_URL`의 데이터베이스 이름이 정확히 맞지 않았다.
- OAuth login과 callback을 같은 `TestClient` 흐름으로 이어 주지 않으면 state cookie가 누락된 것처럼 보였다.

## 수정

- Compose의 DB 이름과 애플리케이션 설정을 같은 문자열로 맞췄다.
- 테스트는 같은 `TestClient` 인스턴스로 login과 callback을 순차 호출하는 패턴으로 정리했다.

## 검증 근거

- 마지막 기록 기준으로 Compose live/ready probe가 다시 통과했다.
- 이 이슈는 보안 로직을 보기 전에 인프라 정합성과 쿠키 전파를 먼저 점검해야 한다는 교훈을 남긴다.

마지막 실제 실행 날짜는 [../../../docs/verification-report.md](../../../docs/verification-report.md)를 따른다.
