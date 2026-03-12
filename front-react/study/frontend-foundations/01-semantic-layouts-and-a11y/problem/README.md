# 문제 정의

프로비넌스: `authored`

## 문제

설정/대시보드 성격의 화면을 만들면서 semantic layout, form grouping, help/error text pairing, keyboard reachable interaction이 실제 DOM 구조에 어떻게 드러나는지 검증 가능한 형태로 구현한다.

## 제공 자산

- 이 문서: 문제 정의와 범위
- `data/`: 추가 입력 데이터가 필요 없는 단계를 위해 placeholder만 유지
- `script/`: 공통 디렉터리 shape를 유지하기 위한 placeholder

## 제약

- React 없이 vanilla DOM과 CSS만 사용한다.
- 정적이지만 상호작용 가능한 UI shell이어야 한다.
- semantic markup과 keyboard reachability가 DOM 구조만 봐도 드러나야 한다.

## 포함 범위

- semantic landmarks
- responsive two-column to single-column layout
- labeled forms
- inline help and error pairing
- keyboard focus states

## 제외 범위

- 복잡한 데이터 fetching
- local persistence
- 실제 라우팅

## 요구 산출물

- `vanilla/`에 실행 가능한 UI shell 구현
- landmark, form, validation 흐름을 설명하는 공개 문서
- 구조적 검증과 keyboard smoke를 포함한 테스트

## Canonical Verification

```bash
cd study
npm run verify --workspace @front-react/semantic-layouts-a11y
```

- `vitest`: shell 구조와 validation helper 확인
- `playwright`: landmark 탐색과 keyboard submission 흐름 확인
