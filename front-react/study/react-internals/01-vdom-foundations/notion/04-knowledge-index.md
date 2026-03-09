# 지식 인덱스

## 핵심 개념 → 문서 연결

| 개념 | 프로젝트 내 문서 | 비고 |
| --- | --- | --- |
| VNode 구조와 동기 렌더 흐름 | `docs/concepts/vdom-and-rendering.md` | createDom → updateDom → 재귀 → append 순서 |
| JSX → createElement 변환 | `docs/concepts/jsx-to-vnode.md` | primitive 정규화, TEXT_ELEMENT |
| 레거시 자산 추적 | `docs/references/legacy-source-map.md` | 원본과 현재 구현의 대응 관계 |

## 핵심 파일 → 역할 요약

| 파일 | 역할 |
| --- | --- |
| `ts/src/types.ts` | VNode, VNodeProps, VNodeType 타입 정의 |
| `ts/src/element.ts` | createElement, createTextElement (VNode 생성) |
| `ts/src/dom-utils.ts` | createDom, updateDom, render (VNode → 실제 DOM) |
| `ts/src/index.ts` | public export barrel |
| `ts/tests/element.test.ts` | createElement, createTextElement 단위 테스트 (10+ 케이스) |
| `ts/tests/dom-utils.test.ts` | createDom, updateDom, render 단위 테스트 (17+ 케이스) |

## 이 프로젝트의 위치

```
react-internals 트랙
├── 01-vdom-foundations       ← 현재
├── 02-render-pipeline        ← diff/patch, render/commit 분리
├── 03-hooks-and-events       ← useState, useEffect, delegated events
└── 04-runtime-demo-app       ← 공유 런타임 위의 demo app
```

- **이전**: `frontend-foundations` 트랙 전체 — innerHTML 교체의 한계를 체감
- **다음**: `02-render-pipeline` — 이 프로젝트의 전체 리렌더 한계를 diff/patch로 해결
- **소비자**: 이 프로젝트의 `createElement`, `createDom`, `updateDom`이 이후 프로젝트에서 shared runtime의 일부로 사용됨
