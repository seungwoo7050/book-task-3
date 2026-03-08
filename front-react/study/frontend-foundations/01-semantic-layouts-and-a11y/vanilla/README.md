# Vanilla Implementation

상태: `verified`

## problem scope covered

- semantic landmarks
- labeled form inputs
- inline help and error pairing
- keyboard validation flow
- responsive multi-column shell

## build command

```bash
cd study
npm run build --workspace @front-react/semantic-layouts-a11y
```

## test command

```bash
cd study
npm run verify --workspace @front-react/semantic-layouts-a11y
```

## current status

- `verified`

## known gaps

- local persistence는 없다.
- 실제 라우팅이나 데이터 fetching은 없다.
- keyboard interaction은 form과 nav 범위로 제한된다.

## implementation notes

- `vanilla/src/app.ts`가 semantic shell 마크업과 validation wiring을 담당한다.
- `vanilla/src/validation.ts`는 field-level 검증 규칙만 분리한다.
- `vanilla/tests/semantic-layout.spec.ts`는 landmark, responsive grid, keyboard-only submission을 확인한다.
