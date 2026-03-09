# 개발 타임라인: 처음부터 검증까지

이 문서는 프로젝트의 전체 개발 과정을 순서대로 기록한다. 소스코드를 읽으면 "무엇이 만들어졌는지"는 알 수 있지만, "어떤 순서로, 어떤 명령어로, 왜 그 시점에 그 결정을 내렸는지"는 코드만으로 알 수 없다. 이 타임라인이 그 빈자리를 채운다.

---

## Phase 0: 프로젝트 스캐폴딩

### 작업 환경 준비

```bash
# 저장소 루트에서 study/ 워크스페이스 초기 설정
cd study
npm install
```

모노레포 구조에서 npm workspaces를 사용한다. `study/package.json`의 `workspaces` 배열에 이 프로젝트 경로(`frontend-foundations/01-semantic-layouts-and-a11y`)가 등록되어 있어서, 루트에서 `npm install` 한 번이면 모든 워크스페이스의 의존성이 설치된다.

### 디렉토리 구조 생성

```
01-semantic-layouts-and-a11y/
├── index.html              # Vite 진입점
├── package.json            # 워크스페이스 패키지 정의
├── vite.config.ts          # 개발 서버 설정
├── vitest.config.ts        # 단위 테스트 설정
├── playwright.config.ts    # E2E 테스트 설정
├── tsconfig.json           # TypeScript 설정
├── problem/                # 문제 명세 (authored brief)
├── vanilla/src/            # 구현 코드
├── vanilla/tests/          # 테스트
└── docs/                   # 공개 문서
```

### 패키지 의존성 설치

```bash
# package.json에 정의된 devDependencies
npm install --save-dev vite typescript vitest jsdom @playwright/test @types/node
```

- **Vite** `^7.1.12`: 빠른 개발 서버와 HMR을 위해
- **Vitest** `^4.0.18`: Vite 기반 테스트 러너 (jsdom 환경)
- **jsdom** `^28.1.0`: vitest에서 DOM API를 사용하기 위한 환경
- **Playwright** `^1.58.2`: 실제 브라우저 기반 E2E 테스트
- **TypeScript** `^5.9.3`: 정적 타입 검사

```bash
# Playwright 브라우저 바이너리 설치 (최초 1회)
npx playwright install
```

### Vite 설정

`vite.config.ts`에서 개발 서버를 `127.0.0.1:4173`에 고정했다. Playwright가 이 주소로 접속해서 E2E 테스트를 돌리기 때문에, 포트가 달라지면 테스트가 깨진다.

---

## Phase 1: 마크업과 시맨틱 구조

### index.html 작성

최소한의 HTML 셸. `<div id="app">`만 놓고, 실제 마크업은 TypeScript에서 동적으로 주입한다.

### vanilla/src/main.ts 작성

진입점 파일. `#app` 컨테이너를 찾아 `mountSettingsShell()`에 넘긴다.

### vanilla/src/app.ts — getAppMarkup() 작성

가장 많은 시간이 들어간 단계. 전체 HTML 마크업을 문자열로 반환하는 함수다. 이 함수에서 결정한 것들:

- **Skip link**: `<a class="skip-link" href="#main-content">` — 키보드 사용자가 내비게이션을 건너뛰고 본문으로 갈 수 있도록
- **Landmark 배치**: header → nav → main → aside 순서
- **Form 구조**: `<fieldset>`으로 그룹핑, `<legend>`로 그룹 제목, 각 필드에 label/help/error 트리플
- **aria-describedby 연결**: 각 input에 help-id와 error-id를 공백으로 구분해서 연결
- **aria-live status 영역**: 폼 하단에 `role="status" aria-live="polite"` 영역 배치

---

## Phase 2: 스타일링

### vanilla/src/styles.css 작성

마크업 구조가 고정된 뒤에 스타일을 입혔다. 주요 결정:

- **CSS Grid 3-column layout**: `grid-template-columns: minmax(220px, 280px) minmax(0, 1fr) minmax(240px, 320px)`
- **반응형 breakpoint**: media query 대신 minmax()에 의존해서 자연스러운 collapse
- **focus-visible outline**: `:focus-visible`로 키보드 포커스 시에만 outline 표시
- **Skip link 스타일**: 기본적으로 화면 밖에 숨겨져 있다가, 포커스 시 상단에 표시

### 개발 서버로 시각 확인

```bash
cd study
npm run dev --workspace @front-react/semantic-layouts-a11y
# → http://127.0.0.1:4173 에서 확인
```

개발 서버를 띄워 놓고 브라우저에서 확인하면서 반복적으로 스타일을 조정했다. 특히 좁은 뷰포트에서 reading order가 유지되는지 DevTools의 반응형 모드로 확인했다.

---

## Phase 3: 인터랙션 로직

### vanilla/src/validation.ts 작성

순수 함수 `validateSettings()`와 `hasValidationErrors()`를 먼저 작성. DOM에 의존하지 않는 로직이라 테스트가 쉽다.

### vanilla/src/app.ts — mountSettingsShell() 작성

`getAppMarkup()`으로 마크업을 삽입한 뒤, 폼 이벤트 핸들러를 연결하는 함수.

1. **submit 핸들러**: `preventDefault()` → 전체 검증 → 에러 시 상태 메시지 + 포커스 이동 / 성공 시 저장 메시지
2. **blur 핸들러**: 각 필드에 blur 이벤트를 걸어서 해당 필드만 부분 검증
3. **updateErrorState()**: `aria-invalid` 설정, error text 노출/숨김
4. **focusFirstInvalidField()**: FIELD_IDS 순서대로 첫 번째 에러 필드에 포커스

---

## Phase 4: 테스트 작성

### vitest 단위 테스트

```bash
cd study
npm run test --workspace @front-react/semantic-layouts-a11y
```

**vanilla/tests/validation.test.ts** (2개 테스트):
- 짧은 workspace name + 잘못된 email → 에러 반환 확인
- 올바른 값 → 빈 에러 객체 확인

**vanilla/tests/shell.test.ts** (3개 테스트):
- mount 후 landmark와 labeled control 존재 확인
- invalid submit 시 aria-invalid, error text, 포커스 이동 확인
- valid submit 시 성공 메시지 확인

### Playwright E2E 테스트

```bash
cd study
npm run e2e --workspace @front-react/semantic-layouts-a11y
```

**vanilla/tests/semantic-layout.spec.ts** (2개 시나리오):
- landmark, label, help text, responsive grid 검증
- 키보드 전용으로 invalid submit → 수정 → 재제출 시나리오

Playwright 설정에서 `webServer` 옵션으로 테스트 실행 전에 자동으로 Vite 개발 서버를 띄운다. 별도로 서버를 미리 실행할 필요가 없다.

---

## Phase 5: 문서 작성과 검증

### docs/ 작성

- `docs/concepts/semantic-layout-decisions.md`: landmark 순서와 반응형 기준에 대한 판단 근거
- `docs/concepts/accessible-form-patterns.md`: label/help/error pairing 패턴
- `docs/references/verification-notes.md`: 테스트 범위와 알려진 한계

### 최종 검증

```bash
cd study
npm run verify --workspace @front-react/semantic-layouts-a11y
# → vitest 5개 테스트 통과
# → playwright 2개 E2E 시나리오 통과
```

검증 일시: 2026-03-08

---

## 사용한 도구 요약

| 도구 | 버전 | 용도 |
| --- | --- | --- |
| Node.js | (워크스페이스 기준) | 런타임 |
| npm | (워크스페이스 기준) | 패키지 관리, 워크스페이스 스크립트 실행 |
| Vite | ^7.1.12 | 개발 서버, 번들링 |
| TypeScript | ^5.9.3 | 정적 타입 검사 |
| Vitest | ^4.0.18 | 단위/DOM 테스트 (jsdom 환경) |
| jsdom | ^28.1.0 | 테스트용 DOM 환경 |
| Playwright | ^1.58.2 | E2E 브라우저 테스트 |
| 브라우저 DevTools | — | 반응형 모드, 접근성 트리 확인 |

## 자주 사용한 CLI 명령어

```bash
# 개발 서버 실행
npm run dev --workspace @front-react/semantic-layouts-a11y

# 단위 테스트 실행
npm run test --workspace @front-react/semantic-layouts-a11y

# E2E 테스트 실행
npm run e2e --workspace @front-react/semantic-layouts-a11y

# 전체 검증 (test + e2e)
npm run verify --workspace @front-react/semantic-layouts-a11y

# Playwright 브라우저 설치 (최초 1회)
npx playwright install

# 테스트 watch 모드
npm run test:watch --workspace @front-react/semantic-layouts-a11y
```
