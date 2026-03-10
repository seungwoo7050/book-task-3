# v0 초기 실행 데모 문서 안내

registry seed, manifest validation, baseline selector, 한국어 추천 근거, offline eval까지 동작하는 최초 runnable 데모다.

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
