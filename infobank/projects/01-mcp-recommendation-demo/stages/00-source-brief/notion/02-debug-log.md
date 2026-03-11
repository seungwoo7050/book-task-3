# 00 문제 정의와 기준 문서 디버그 기록

## 먼저 확인할 명령

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm dev
pnpm test
pnpm eval
pnpm capture:presentation
pnpm e2e
```

## 다시 막히기 쉬운 지점

- 상위 `README.md`, `problem/README.md`, `docs/README.md`, 연결된 capstone 경로 설명이 서로 어긋나지 않는지 먼저 확인한다.
- `v0-initial-demo`가 아니라 다른 버전의 코드를 보고 있으면 stage 목적이 흐려질 수 있다.
- 이 단계는 문서 단계다. 별도 구현 디렉터리를 만들기보다, 어떤 코드를 읽어야 하는지 정확히 가리키는 것이 더 중요하다.

## 현재 상태 메모

- 별도 구현 디렉터리를 만들지 않고, capstone 코드를 읽기 위한 기준 문서 단계로 유지한다.
- 실제 동작 코드는 `v0-initial-demo`에서 시작하고, 이 stage는 그 코드를 이해하기 위한 상위 설명을 맡는다.

## 재현 실패 시 다시 볼 경로

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/catalog.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/eval.ts`
- `../../docs/curriculum/reference-spine.md`
- `../../docs/curriculum/project-selection-rationale.md`
