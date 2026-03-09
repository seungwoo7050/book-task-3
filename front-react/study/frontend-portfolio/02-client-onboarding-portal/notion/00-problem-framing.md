# 문제 정의 — Client Onboarding Portal

## 왜 이 프로젝트인가

포트폴리오의 첫 번째 프로젝트인 Ops Triage Console은 B2B 내부 도구형 UI를 다뤘다. 데이터 테이블, 필터, bulk action, 낙관적 업데이트처럼 "운영자가 빠르게 처리하는" 패턴에 집중했다. 그런데 프론트엔드 개발자가 만드는 제품의 절반 이상은 고객이 직접 사용하는 화면이다. 가입, 설정, 초대, 제출 같은 "단계별로 안내하는" 흐름은 내부 도구와 전혀 다른 판단이 필요하다.

Client Onboarding Portal은 이 빈자리를 채운다. SaaS 고객이 첫 로그인 후 workspace를 설정하고, 팀원을 초대하고, 최종 제출까지 마치는 온보딩 여정을 구현한다.

## 사용자 시나리오

SaaS 서비스에 가입한 기업 고객이 있다. 이 고객은:

1. **로그인한다** — 이메일과 비밀번호로 세션을 생성한다.
2. **workspace를 설정한다** — 회사명, 산업, 리전, 팀 규모, 컴플라이언스 담당자 이메일을 입력한다.
3. **팀원을 초대한다** — 첫 번째 collaborator의 이메일과 역할을 지정한다.
4. **리뷰하고 제출한다** — 입력한 정보를 확인하고, 체크리스트를 완료한 뒤 제출한다.

이 흐름에서 핵심 요구사항은:
- 미인증 사용자가 `/onboarding`에 직접 접근하면 로그인 안내로 막아야 한다(route guard).
- 프로필 정보는 저장 후 새로고침해도 유지되어야 한다(draft restore).
- 입력을 잘못하면 말해 줘야 한다(field validation).
- 제출이 실패하면 다시 시도할 수 있어야 한다(submit retry).

## 이 프로젝트가 보여 주는 역량

### form validation과 schema-first 설계

Zod 4로 세 가지 스키마(signIn, workspaceProfile, inviteInput)를 정의하고, React Hook Form의 `zodResolver`로 연결했다. 이메일 형식, 최소 글자 수, 필수 선택 같은 제약 조건은 스키마에 한 번만 작성하면 폼과 서비스 양쪽에서 재사용된다.

### 다단계 wizard 흐름

세 개의 step(workspace → invites → review)을 URL query parameter(`?step=`)로 관리한다. 뒤로가기, 앞으로가기, 직접 URL 입력 모두 올바른 step으로 안내된다. `coerceStep` 함수가 유효하지 않은 step 값을 기본값으로 보정한다.

### session gate와 route guard

`/onboarding` 경로는 세션이 없으면 접근할 수 없다. React Query의 session 쿼리 결과에 따라 조건부 렌더링으로 처리했다. 별도의 middleware나 서버 리다이렉트 없이, 컴포넌트 레벨에서 guard를 구현했다.

### draft save와 복원

workspace profile을 localStorage에 저장하고, 페이지를 새로고침하면 React Query가 다시 읽어 폼에 채운다. `useForm`의 `reset`을 `profileQuery.data` 변경 시 호출해 sync를 맞춘다.

### submit lifecycle — 실패, 재시도, 성공

제출 시 의도적 실패를 시뮬레이션할 수 있는 체크박스를 제공한다. 실패하면 에러 메시지가 표시되고, 같은 버튼으로 재시도하면 성공한다. pending, error, success 세 가지 상태를 명시적으로 관리한다.

## 기술 스택 선택 근거

| 기술 | 이유 |
|------|------|
| Next.js 16 (App Router) | 라우팅, 레이아웃, SSR 기반 확보 |
| React 19 | 최신 렌더링 모델 활용 |
| React Hook Form + zodResolver | 폼 상태와 검증을 한 곳에서 관리 |
| TanStack React Query | 세션/프로필/초대/체크리스트 캐시 |
| Zod 4 | 런타임 검증과 커스텀 에러 메시지 |
| Tailwind CSS 4 | 유틸리티 기반 스타일, 커스텀 디자인 |
| Manrope + IBM Plex Mono | 본문과 라벨/코드를 시각적으로 구분 |

## Ops Triage Console과의 차이

Ops Triage Console은 "데이터를 빠르게 처리하는" 도구다. 사용자가 이미 도메인을 알고 있으므로 테이블, 필터, 단축키가 중요하다.

Client Onboarding Portal은 "처음 사용하는 고객을 안내하는" 제품이다. 사용자가 무엇을 해야 하는지 모르므로, 단계 진행 표시, 체크리스트, 입력 안내가 중요하다. 기술적으로도 React Hook Form, 다단계 wizard, route guard 같은 다른 패턴이 필요하다.
