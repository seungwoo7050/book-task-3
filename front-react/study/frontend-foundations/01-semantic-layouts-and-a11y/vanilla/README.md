# Vanilla 구현

상태: `verified`

## 이 구현이 답하는 범위

- semantic landmarks
- labeled form inputs
- inline help and error pairing
- keyboard validation flow
- responsive multi-column shell

## 핵심 파일

- `src/app.ts`: semantic shell 마크업과 validation wiring
- `src/validation.ts`: field-level 검증 규칙
- `tests/semantic-layout.spec.ts`: landmark, responsive grid, keyboard submission smoke

## 실행과 검증

```bash
cd study
npm run build --workspace @front-react/semantic-layouts-a11y
npm run verify --workspace @front-react/semantic-layouts-a11y
```

## 현재 한계

- local persistence는 없다.
- 실제 라우팅이나 데이터 fetching은 없다.
- keyboard interaction은 form과 navigation 범위로 제한된다.
