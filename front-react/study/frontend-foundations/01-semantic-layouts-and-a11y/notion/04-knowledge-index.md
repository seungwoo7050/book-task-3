# 지식 인덱스: 이 프로젝트에서 연결되는 것들

## 핵심 개념 → 문서 연결

| 개념 | 프로젝트 내 문서 | 비고 |
| --- | --- | --- |
| Landmark와 reading order 설계 | `docs/concepts/semantic-layout-decisions.md` | header, nav, main, aside를 왜 이 순서로 배치했는지 |
| Label/help/error pairing | `docs/concepts/accessible-form-patterns.md` | aria-describedby와 hidden error element 패턴 |
| 검증 전략과 한계 | `docs/references/verification-notes.md` | vitest vs Playwright 역할 분리 |

## 핵심 파일 → 역할 요약

| 파일 | 역할 |
| --- | --- |
| `vanilla/src/app.ts` | 마크업 생성 + 폼 이벤트 핸들링 (mount 함수) |
| `vanilla/src/validation.ts` | 순수 함수 기반 폼 검증 로직 |
| `vanilla/src/main.ts` | 앱 진입점 (컨테이너 연결) |
| `vanilla/src/styles.css` | 반응형 grid, focus-visible, 시각 디자인 |
| `vanilla/tests/shell.test.ts` | DOM 구조 + 폼 상호작용 단위 테스트 |
| `vanilla/tests/validation.test.ts` | validation 로직 단위 테스트 |
| `vanilla/tests/semantic-layout.spec.ts` | Playwright E2E (landmark, 키보드 흐름, 반응형) |

## 이 프로젝트의 위치

```
frontend-foundations 트랙
├── 01-semantic-layouts-and-a11y  ← 현재
├── 02-dom-state-and-events       ← DOM 상태, 이벤트 전파, 영속성
└── 03-networked-ui-patterns      ← 비동기RUI, abort, retry
```

- **이전**: 없음 (시작점)
- **다음**: `02-dom-state-and-events` — 이 프로젝트에서 다루지 않은 DOM 상태 동기화, 이벤트 위임, localStorage/URL 상태를 이어받는다.
- **상위 참조**: `react-internals` 트랙이 이 기초 위에서 Virtual DOM과 reconciliation을 다룬다.

## 외부 참고 자료 (학습 중 참조한 것)

- [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) — form 패턴과 landmark 역할 기준
- [MDN: Using ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA) — aria-describedby, aria-live 동작 방식
- [Inclusive Components by Heydon Pickering](https://inclusive-components.design/) — hidden error element 패턴의 출처
