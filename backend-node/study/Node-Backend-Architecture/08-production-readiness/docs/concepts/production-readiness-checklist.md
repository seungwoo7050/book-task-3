# Production Readiness Checklist

이 프로젝트는 "운영 준비"를 한 번에 완성하는 대신, 초보가 바로 볼 수 있는 최소 경계를 만든다.

- Config: 잘못된 환경 변수는 가능한 한 빨리 실패해야 한다.
- Health vs readiness: 프로세스 생존 여부와 의존성 준비 여부를 구분해야 한다.
- Logging: 사람이 읽을 로그보다 기계가 수집하기 쉬운 구조화 로그가 우선이다.
- Docker: 로컬과 CI에서 같은 빌드 경로를 타야 한다.
- CI: 최소한 build, unit, e2e를 자동으로 돌려야 "검증했다"는 말을 할 수 있다.

rate limiting, cache, queue는 여기서 전체 구현까지 밀어붙이지 않는다.
대신 어느 시점에 도입해야 하는지, 어떤 실패 신호가 나오면 고려해야 하는지 문서로 남긴다.
