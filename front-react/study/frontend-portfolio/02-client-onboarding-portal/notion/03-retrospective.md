# 회고 — Client Onboarding Portal을 만들며 배운 것

## 프로젝트 개요

SaaS 고객의 첫 온보딩 여정을 구현했다. sign-in → workspace 설정 → 팀원 초대 → 리뷰/제출의 4단계를 하나의 wizard 흐름으로 만들었다. Ops Triage Console이 "내부 운영자의 효율"을 다뤘다면, 이 프로젝트는 "고객의 불안을 줄이고 다음 행동을 안내하는 것"을 다뤘다.

## 잘한 점

### React Hook Form + Zod의 궁합

폼 상태 관리를 React Hook Form에 맡기고, 검증은 Zod에 위임한 결정이 좋았다. `zodResolver`가 이 둘을 연결해 주므로, 폼 코드에서는 validation 로직을 직접 작성할 필요가 없었다. 에러 메시지도 Zod 스키마에서 한 번만 정의하면 폼과 서비스 양쪽에서 일관되게 사용된다.

`useForm`의 `register` 함수가 반환하는 props를 `<input>`에 spread하면, 폼 값 추적, 더티 상태, validation trigger가 자동으로 연결된다. controlled component 패턴의 `useState` + `onChange` 보일러플레이트를 완전히 제거했다.

### controlled step 관리

step을 component 내부 state로 관리하지 않고, URL query parameter로 올려 보낸 것이 좋았다. `OnboardingRoute`에서 `useSearchParams`로 step을 읽고 `router.replace`로 변경한다. 이렇게 하면:
- 브라우저 주소 표시줄이 현재 step을 반영한다.
- 특정 step으로 직접 링크할 수 있다(route guard가 허용하는 범위 내에서).
- `ClientOnboardingPortal`은 pure controlled component가 되어 테스트가 쉽다.

### 세션 기반 조건부 쿼리

`profileQuery`, `invitesQuery`, `checklistQuery`의 `enabled` 옵션에 `Boolean(sessionQuery.data)`를 넣은 것이 효과적이었다. 세션이 없으면 불필요한 API 호출이 발생하지 않고, 세션이 생기는 순간 세 쿼리가 동시에 시작된다. React Query의 `enabled`는 선언적 의존성 표현으로, 수동 조건 분기보다 깔끔하다.

### Field / SummaryCard 추출

반복되는 폼 필드 래퍼를 `Field` 컴포넌트로, 리뷰 요약을 `SummaryCard` 컴포넌트로 추출했다. 각각 20줄 미만의 간단한 추출이지만, 메인 컴포넌트의 JSX를 크게 줄였다.

## 부족했던 점

### 메인 컴포넌트의 크기

`ClientOnboardingPortal`이 약 560줄이다. 쿼리 4개, 폼 2개, mutation 5개, useState 4개가 한 컴포넌트에 모여 있다. step별로 렌더링을 분기하는 구조라서 한 파일에 넣는 것이 자연스럽기는 하지만, `WorkspaceStep`, `InviteStep`, `ReviewStep` 컴포넌트로 분리했으면 각 step의 책임이 더 명확했을 것이다.

### auto-save 미구현

프로필 저장이 `Save draft` 버튼을 명시적으로 누르는 방식이다. 사용자가 저장 없이 다른 step으로 이동하면 입력 내용이 사라진다. 디바운스 auto-save가 있었으면 더 자연스러웠겠지만, "언제 저장되는지 사용자에게 명확하게 알려 주는 것"을 우선했으므로 트레이드오프로 받아들일 수 있다.

### 체크리스트 로직의 암묵적 결합

`saveProfileMutation`이 프로필을 저장하면서 동시에 `completeChecklistItem("profile")`도 호출한다. 프로필 저장과 체크리스트 완료가 한 mutation에 묶여 있어서, "프로필은 저장했지만 체크리스트는 완료하지 않기"가 불가능하다. 현재 요구사항에서는 문제없지만, 체크리스트가 독립적으로 동작해야 하는 경우에는 분리가 필요하다.

### invite 삭제 기능 부재

invite를 추가한 후 삭제하는 기능이 없다. 실수로 잘못된 이메일을 추가하면 되돌릴 수 없다. 데모 범위에서는 "추가"만 보여 주면 충분하다고 판단했지만, 실제 제품이라면 반드시 필요한 기능이다.

## 기술적 인사이트

### controlled vs uncontrolled wizard

wizard를 만들 때 "step을 누가 관리하느냐"가 첫 번째 결정이다. 이 프로젝트에서는 URL(router)이 관리한다. 다른 선택지로는:
- `useState`(컴포넌트 내부) — 가장 단순하지만 URL 공유 불가
- `useReducer`(상태 머신) — 전환 규칙이 복잡할 때
- 서버 state(DB) — multi-session resumption이 필요할 때

현재 규모에서는 URL query parameter가 적절하다.

### React Hook Form의 reset 타이밍

`useForm`의 `defaultValues`는 컴포넌트 마운트 시 한 번만 적용된다. 비동기 데이터(React Query 결과)를 폼에 채우려면 `useEffect` + `reset`이 필요하다. React Hook Form v7의 `values` prop을 사용하면 effect 없이도 되지만, reset이 더 명시적이고 "언제 폼이 초기화되는지"가 코드에서 바로 보인다.

### submit lifecycle의 상태 관리

submit은 네 가지 상태를 가진다: idle, pending, error, success. `useMutation`이 pending을 자동으로 관리하고, error/success는 callback에서 로컬 state(`submitError`, `submitResult`)로 관리한다. 이 두 가지를 혼합하는 것이 약간 어색하지만, React Query의 mutation은 "최근 mutation 1건"의 상태만 추적하므로, 에러와 결과를 UI에서 동시에 보여 줄 필요가 있을 때 로컬 state가 필요해진다.

### route guard의 계층

이 프로젝트는 컴포넌트 레벨 guard를 사용한다. Next.js middleware나 server component에서 리다이렉트하는 방법도 있지만, mock backend에서는 서버 측 세션 검증이 불가능하다. 클라이언트에서 React Query로 세션을 확인하고 조건부 렌더링하는 방식이 현실적이다.

## Ops Triage Console과의 비교

| 관점 | Ops Triage Console | Client Onboarding Portal |
|------|-------------------|--------------------------|
| 사용자 | 내부 운영자 | 외부 고객 |
| 핵심 패턴 | 데이터 테이블, 낙관적 업데이트 | 폼 wizard, draft save |
| 상태 관리 복잡도 | 높음 (7 useState + 캐시 3종) | 중간 (4 useState + 쿼리 4개) |
| 폼 라이브러리 | 없음 (직접 관리) | React Hook Form |
| UI 라이브러리 | Radix UI 래퍼 11개 | 네이티브 HTML |
| 에러 처리 | 카오스 엔지니어링 | 1회 실패 시뮬레이션 |

## 다음에 다르게 하고 싶은 것

1. **step 분리** — 각 step을 별도 컴포넌트 파일로 분리하고, shared context로 데이터 연결
2. **auto-save** — debounced 프로필 저장으로 UX 향상
3. **invite 삭제** — 추가한 invite를 제거하는 기능
4. **progress indicator** — step 진행 비율을 시각적으로 표시하는 progress bar
5. **accessibility** — 키보드만으로 전체 wizard를 완주하는 E2E 테스트 추가
