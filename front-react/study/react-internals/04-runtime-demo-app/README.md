# 04 Runtime Demo App

상태: `verified`

이 프로젝트는 `legacy/platform-capstone`을 공유 런타임 소비 구조로 다시 해석해, 작은 demo app과 성능/한계 문서화를 함께 다루는 마지막 단계다.

## 왜 주니어 경로에 필요한가

internals 학습은 실제 기능 조합 위에서 한계와 tradeoff를 확인할 때 더 설득력 있다. 이 단계는 직접 만든 runtime이 어디까지 설명 가능하고 어디서 멈추는지 보여 주는 마감 단계다.

## Prerequisite

- `03-hooks-and-events`
- runtime integration 이해

## 구조

- `problem/`: 레거시 capstone 원문과 제공 자산 위치
- `ts/`: demo app과 runtime integration 실험 자리
- `docs/`: 성능/한계 문서
- `notion/`: 로컬 전용 과정 로그

## Build/Test Command

```bash
cd study
npm run dev --workspace @front-react/runtime-demo-app
npm run test --workspace @front-react/runtime-demo-app
npm run typecheck --workspace @front-react/runtime-demo-app
npm run verify --workspace @front-react/runtime-demo-app
```

검증 범위는 아래와 같다.

- shared runtime import 경계 유지
- debounced search와 결과 축소
- load more 기반 paginated interaction
- render metrics panel 갱신

## 다음 단계로 이어지는 한계

이 트랙은 internals 기반 demo app까지를 다루며, 실제 채용용 제품형 UI 신호는 `frontend-portfolio` 트랙이 이어받는다.
