# Contributing

이 저장소는 study-first repository다. 특히 `legacy/`는 읽기 전용 참조이고, 실제 개선은 `study*/` 아래에서 진행한다.

## Ground Rules

- `legacy/`는 수정하지 않는다.
- 구조 변경은 tracked README와 build/test 명령을 함께 갱신한다.
- generated noise (`.venv`, `node_modules`, local DB, caches)는 커밋하지 않는다.
- 재현 가능한 명령과 실제 파일 경로를 기준으로 설명한다.

## Study2 v3

`study2/08-capstone-submission/v3-self-hosted-oss`는 현재 self-hosted OSS target이다.

기여 시 우선 확인할 것:

1. `README.md`
2. `study2/README.md`
3. `study2/08-capstone-submission/v3-self-hosted-oss/README.md`

## Validation

`study2` 변경은 가능한 한 해당 버전 디렉터리에서 아래를 확인한다.

```bash
cd study2/08-capstone-submission/v3-self-hosted-oss/python
UV_PYTHON=python3.12 uv sync --extra dev
UV_PYTHON=python3.12 make gate-all
```

프론트 단독 확인:

```bash
cd study2/08-capstone-submission/v3-self-hosted-oss/react
pnpm install
pnpm test --run
```
