# 개발 타임라인: 처음부터 검증까지

---

## Phase 0: 프로젝트 스캐폴딩

### 디렉토리 구조

```
01-vdom-foundations/
├── package.json            # @front-react/vdom-foundations
├── tsconfig.json
├── vitest.config.ts
├── problem/                # 레거시 원문, 스켈레톤 코드
│   ├── original/           # 원본 README
│   ├── code/               # 참고용 스켈레톤
│   ├── data/
│   └── script/             # Makefile (adapted)
├── ts/                     # 현재 구현
│   ├── src/
│   └── tests/
└── docs/                   # 공개 문서
```

### 의존성 설치

```bash
cd study
npm install
```

이 프로젝트의 devDependencies:
- **TypeScript** `^5.3.0`: 정적 타입
- **Vitest** `^1.6.0`: 테스트 러너
- **jsdom** `^24.0.0`: DOM API 테스트 환경

주의: 이 프로젝트는 Vite 개발 서버가 없다 (브라우저 앱이 아니라 라이브러리). Playwright도 없다. 순수 로직과 DOM 조작 테스트만 존재한다.

### 레거시 자산 확인

```bash
# problem/original/README.md로 원본 문제 명세 확인
# problem/code/로 스켈레톤 코드 참고
```

기존 학습 자료의 아이디어를 가져오되, TypeScript로 재작성하고 테스트를 새로 작성했다.

---

## Phase 1: 타입 정의

### ts/src/types.ts 작성

최소 VNode 인터페이스 정의:
- `VNode`: `{ type: VNodeType, props: VNodeProps }`
- `VNodeType`: `string | Function` (Function은 미래 함수 컴포넌트를 위해)
- `VNodeProps`: `{ [key: string]: any, children: VNode[] }`

이 타입이 전체 트랙의 기초가 된다. 이후 프로젝트에서도 이 인터페이스를 확장/재사용한다.

---

## Phase 2: VNode 생성 함수

### ts/src/element.ts 작성

두 함수를 구현:

1. **`createTextElement(text)`**: 문자열을 `{ type: "TEXT_ELEMENT", props: { nodeValue: text, children: [] } }`로 변환
2. **`createElement(type, props, ...children)`**: JSX 변환 목표 함수. null props → 빈 객체, primitive children → createTextElement 호출

### 테스트 작성: ts/tests/element.test.ts

```bash
npm run test --workspace @front-react/vdom-foundations
```

10개 테스트 케이스:
- createTextElement: TEXT_ELEMENT 생성, 빈 문자열 처리
- createElement: 타입 설정, props 병합, null props, children 배열, 문자열/숫자 래핑, VNode 유지, 혼합 children, 깊은 중첩

---

## Phase 3: DOM 생성과 업데이트

### ts/src/dom-utils.ts 작성

세 함수를 순서대로 구현:

1. **`createDom(vnode)`**: TEXT_ELEMENT → `createTextNode()`, 그 외 → `createElement()`. 생성 직후 `updateDom()` 호출.

2. **`updateDom(dom, prevProps, nextProps)`**: prop 변경을 네 단계로 처리:
   - 이전 이벤트 리스너 제거 (바뀌었거나 사라진 것)
   - 사라진 일반 prop 제거 (빈 문자열로 초기화)
   - 새/변경된 일반 prop 설정
   - 새 이벤트 리스너 추가
   - 헬퍼: `isEvent(key)`, `isProperty(key)`, `isNew(prev, next)`, `isGone(prev, next)`

3. **`render(element, container)`**: createDom → children 재귀 → appendChild

### 테스트 작성: ts/tests/dom-utils.test.ts

17개 테스트 케이스:
- createDom: Text node 생성, HTMLElement 생성, className 적용
- updateDom: prop 설정/제거/변경, 변하지 않은 prop 유지, 이벤트 추가/제거/교체, children 키 무시
- render: 단순 텍스트, 중첩 요소, 속성 반영, 깊은 트리, 이벤트 바인딩

---

## Phase 4: public API 정리

### ts/src/index.ts 작성

barrel export:
- `createDom`, `render`, `updateDom` (from dom-utils)
- `createElement`, `createTextElement` (from element)
- `VNode`, `VNodeProps`, `VNodeType` types

`package.json`의 `exports` 필드: `".": "./ts/src/index.ts"` — 다음 프로젝트에서 이 패키지를 워크스페이스 import로 사용할 수 있게 설정.

---

## Phase 5: 문서 작성

### docs/concepts/
- `vdom-and-rendering.md`: VNode 구조, 동기 렌더 순서, updateDom 단계, 한계
- `jsx-to-vnode.md`: JSX → createElement → VNode 정규화 흐름

### docs/references/
- `legacy-source-map.md`: 원본 자산과 현재 구현의 대응 관계

---

## Phase 6: 최종 검증

```bash
cd study
npm install
npm run verify:vdom
# → 2개 테스트 파일, 27개 테스트 통과
# → npm run typecheck:vdom 통과
```

검증 일시: 2026-03-07

---

## 사용한 도구 요약

| 도구 | 버전 | 용도 |
| --- | --- | --- |
| TypeScript | ^5.3.0 | 정적 타입 (VNode 인터페이스 설계가 핵심) |
| Vitest | ^1.6.0 | 단위 테스트 (jsdom 환경) |
| jsdom | ^24.0.0 | document.createElement, addEventListener 등 DOM API |
| npm workspaces | — | 이 패키지를 다음 프로젝트에서 import 가능하게 설정 |

## 자주 사용한 CLI 명령어

```bash
# 테스트 실행
npm run test --workspace @front-react/vdom-foundations

# 타입 체크
npm run typecheck --workspace @front-react/vdom-foundations

# 전체 검증 (test + typecheck)
npm run verify:vdom

# watch 모드
npm run test:watch --workspace @front-react/vdom-foundations
```
