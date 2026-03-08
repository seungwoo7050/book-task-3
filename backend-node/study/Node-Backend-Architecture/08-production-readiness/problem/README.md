# Problem

## 목표

애플리케이션 코드가 아닌 운영 관점의 기본기를 별도 프로젝트로 다룬다.

## 과제

1. 환경 변수에서 런타임 설정을 읽고 기본값/검증 규칙을 적용한다.
2. `GET /health`와 `GET /ready`를 분리해 liveness와 readiness를 구분한다.
3. 요청 로그를 구조화된 JSON 한 줄로 남긴다.
4. 로컬 실행용 Dockerfile과 CI 초안을 작성한다.
5. rate limiting, cache, queue는 구현보다 운영 판단 기준을 문서에 남긴다.

## 제공 자료

- `problem/code/.env.example`: 예시 환경 변수
- `problem/code/github-actions-ci.example.yml`: CI 초안
- `problem/script/run-checks.sh`: 수동 검증 명령

## 최소 성공 기준

- 잘못된 env 값이면 앱이 빠르게 실패한다.
- `/health`는 항상 200, `/ready`는 config에 따라 200 또는 503을 반환한다.
- 요청 하나당 한 줄의 구조화 로그가 남는다.
- 테스트가 config, health, readiness를 모두 검증한다.
