# v1 랭킹 강건화 문서 안내

v0를 바탕으로 reranker, usage logs, feedback loop, baseline/candidate compare를 더한 운영형 추천 버전이다.

## 포함된 문서

- `docs/README.md`
- `docs/presentation-deck.md`
- `docs/presentation-assets/`
- `problem/README.md`

## 이 문서들이 맡는 역할

- tracked docs는 실행 순서, 검증 기준, 발표 자료처럼 오래 남길 증빙을 맡는다.
- 더 긴 시행착오와 판단 과정은 `notion/`에서 이어서 본다.
- 학생 입장에서는 이 문서 묶음을 그대로 따라가면 자신의 포트폴리오용 제출 문서 세트를 구성할 수 있다.

## 자주 쓰는 명령

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
