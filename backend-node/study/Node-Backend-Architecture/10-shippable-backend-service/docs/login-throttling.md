# Login Throttling

## 규칙

- key: `auth:login:<clientId>`
- 저장소: Redis
- 기본 window: 60초
- 기본 최대 실패 횟수: 5회

`clientId`는 우선 `x-forwarded-for`에서 가져오고, 없으면 `username:<username>` 형식으로 대체한다.

## 동작 흐름

1. 로그인 요청이 들어오면 현재 clientId의 실패 횟수를 먼저 확인한다.
2. 이미 임계치를 넘었으면 즉시 `429`를 반환한다.
3. 비밀번호가 틀리면 실패 횟수를 증가시킨다.
4. 증가 후 임계치에 도달하면 그 요청부터 `429`를 반환한다.
5. 로그인에 성공하면 해당 key를 삭제한다.

## 왜 IP 기반 단순화로 충분한가

- 이 과제는 보안 제품이 아니라 포트폴리오 서비스다.
- 계정 기반, IP 기반, user-agent 기반을 조합한 정교한 throttling은 다음 단계로 남겨 둔다.
- 여기서는 “Redis를 이용해 auth failure state를 관리할 수 있다”는 점을 분명히 보여 주는 것이 중요하다.
