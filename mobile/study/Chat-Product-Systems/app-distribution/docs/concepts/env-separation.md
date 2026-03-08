# Env Separation

채널은 `development`, `staging`, `production` 세 가지로 고정한다.

- `development`: 로컬 개발 서버와 verbose logging
- `staging`: QA와 signed rehearsal
- `production`: store release 후보

예시 env 파일은 실제 비밀값 대신 placeholder만 담고, 같은 키 집합을 유지한다.
리허설 스크립트는 이 키 집합이 어긋나면 실패한다.
