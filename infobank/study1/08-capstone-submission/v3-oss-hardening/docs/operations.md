# Operations

## Bootstrap

```bash
pnpm db:up
pnpm migrate
pnpm seed
pnpm bootstrap:owner
```

`bootstrap:owner`는 `BOOTSTRAP_OWNER_EMAIL`, `BOOTSTRAP_OWNER_PASSWORD`를 읽어 owner 계정을 upsert한다. 이미 존재하면 password hash와 활성 상태를 보정한다.

## Job Model

동기 요청으로 남겨둔 것은 recommendation뿐이다. 아래는 모두 job으로 큐에 넣고 worker가 처리한다.

- eval
- compare
- compatibility
- release-gate
- artifact-export

Job 상태는 `pending -> running -> completed|failed`로 저장되고, 콘솔은 `/api/jobs/:id`를 poll한다.

## Metrics And Readiness

- `/healthz`: 프로세스 생존 확인
- `/readyz`: settings와 DB 준비 상태 확인
- `/metrics`: users/job status 수를 간단한 Prometheus 형식으로 노출

## Audit Review

owner는 Audit Log 화면에서 최근 actor/action/target을 바로 확인할 수 있다. 이 로그는 실험 비교 결과보다 “누가 운영 상태를 바꿨는가”를 추적하는 용도로 둔다.

## Common Operator Flow

1. owner 또는 operator 로그인
2. catalog export 후 변경본 import
3. candidate recommendation으로 운영 근거 확인
4. compare, compatibility, release gate를 순차 실행
5. artifact export로 제출/공유용 Markdown 생성
