# 01 Semantic Layouts And A11y

상태: `verified`

## 무슨 문제인가

설정/대시보드 성격의 화면을 만든다고 해도 semantic landmarks, form grouping, help/error text pairing, keyboard reachable interaction이 먼저 설계되어야 한다. 이 프로젝트는 "읽히는 구조"와 "탐색 가능한 상호작용"을 vanilla DOM만으로 구현하는 문제를 푼다.

## 왜 필요한가

React나 디자인 시스템을 쓰더라도 의미 구조와 접근성이 약하면 제품 품질이 바로 흔들린다. 이 단계는 이후 상태 관리나 비동기 UI로 넘어가기 전에, 브라우저가 기본적으로 제공하는 구조적 품질을 먼저 몸에 익히는 시작점이다.

## 내가 만든 답

semantic landmarks, labeled form, inline help/error, keyboard-friendly validation flow를 갖춘 설정형 UI shell을 `vanilla/`로 구현했다.

- 문제 정의: [problem/README.md](problem/README.md)
- 구현 상세: [vanilla/README.md](vanilla/README.md)
- 공개 문서: [docs/README.md](docs/README.md)

## 핵심 구현 포인트

- `vanilla/src/app.ts`에서 semantic shell 마크업과 validation wiring을 함께 구성한다.
- `vanilla/src/validation.ts`에서 field-level 검증 규칙을 순수 함수로 분리한다.
- `vanilla/tests/semantic-layout.spec.ts`, `shell.test.ts`, `validation.test.ts`로 landmark, 구조, 검증 흐름을 나눠 확인한다.

## 검증

```bash
cd study
npm run dev --workspace @front-react/semantic-layouts-a11y
npm run verify --workspace @front-react/semantic-layouts-a11y
```

- 검증 기준일: 2026-03-08
- `vitest`: shell 구조와 validation 규칙 `5`개 테스트 통과
- `playwright`: landmark 탐색과 keyboard submission `2`개 시나리오 통과

## 읽기 순서

1. [problem/README.md](problem/README.md)
2. [vanilla/README.md](vanilla/README.md)
3. [docs/README.md](docs/README.md)

## 한계

- local persistence, 실제 라우팅, 데이터 fetching은 아직 없다.
- keyboard interaction은 form과 navigation의 핵심 흐름까지만 다룬다.
- 다음 단계인 `02-dom-state-and-events`에서 상태 동기화와 이벤트 orchestration을 본격적으로 다룬다.
