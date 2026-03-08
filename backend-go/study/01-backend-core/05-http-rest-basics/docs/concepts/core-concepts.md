# Core Concepts

## 핵심 개념

- `GET /v1/healthcheck`는 서비스 생존 여부를 확인하는 최소 endpoint다.
- 생성 성공은 `201`, 같은 idempotency key 재시도는 `200`으로 분리했다.
- validation 실패는 `422`로, 잘못된 JSON이나 path parameter는 `400`으로 다루는 편이 읽기 쉽다.
- pagination은 작은 예제에서도 응답 shape와 query parameter 처리 감각을 만든다.

## Trade-offs

- in-memory store는 입문 속도를 높이지만 persistence 이슈를 숨긴다.
- idempotency key 저장을 메모리에 두면 동작은 보이지만 프로세스 재시작에는 약하다.

## 실패하기 쉬운 지점

- `Idempotency-Key`가 없을 때와 중복일 때의 응답 코드를 혼동하기 쉽다.
- page/page_size를 음수나 0으로 넣었을 때 fallback 규칙을 빼먹기 쉽다.

