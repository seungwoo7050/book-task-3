# 00-language-and-typescript structure plan

이 문서는 TypeScript 문법 요약처럼 읽히기보다, 이후 프로젝트들이 기대하는 입력·출력 계약의 출발점처럼 읽혀야 한다. 글의 중심은 "타입을 배웠다"가 아니라 "정규화된 내부 표현을 먼저 세웠다"에 둔다.

## 읽기 구조

1. 이 프로젝트가 왜 bridge의 첫 장면인지 짧게 설명한다.
2. `normalizeTags`, `toNormalizedBook`로 정규화 경계를 먼저 세운 장면을 잡는다.
3. `fetchInventorySnapshot`에서 항목별 실패 격리를 보여 준다.
4. `runCli`에서 종료 코드와 stderr/stdout 계약으로 마무리한다.

## 반드시 남길 근거

- `normalizeTags`와 `toNormalizedBook`
- `fetchInventorySnapshot`
- `runCli`
- `pnpm run build`
- `pnpm run test`
- `pnpm start -- --title ...`

## 리라이트 톤

- "처음부터 구조를 알고 있었다"는 느낌을 줄이지 않는다.
- 설명은 짧게, 판단이 바뀐 순간은 선명하게 남긴다.
- 코드가 왜 전환점이었는지 문단으로 풀고, 템플릿식 라벨 반복은 줄인다.
