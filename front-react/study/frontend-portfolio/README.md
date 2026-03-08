# Frontend Portfolio Track

이 트랙은 학습용 internals 구현과 별개로, 제품형 프론트 포지션 지원에 직접 사용할 메인 포트폴리오를 만드는 공간이다.

## 목적

- 실제 제품 UI 완성도
- 데이터가 많은 운영 화면 설계
- 상태 관리와 optimistic update
- 접근성, 테스트, 문서 품질
- 배포 가능한 결과물

## 프로젝트 목록

| 순서 | 프로젝트 | 상태 | 설명 |
| --- | --- | --- | --- |
| 01 | [01-ops-triage-console](01-ops-triage-console/README.md) | verified | 운영자가 많은 이슈를 빠르게 분류하고 조치하는 B2B triage console |
| 02 | [02-client-onboarding-portal](02-client-onboarding-portal/README.md) | verified | SaaS 고객의 onboarding, workspace setup, invite, submission을 다루는 고객-facing 포털 |

## internals 트랙과의 관계

- `react-internals`는 보조 학습 근거다.
- 이 트랙은 채용용 메인 결과물을 만드는 목적이므로, custom runtime을 전면에 내세우지 않는다.
- 포트폴리오 앱은 실제 제품 UX, 데이터 흐름, 품질 기준을 우선한다.

## 이 트랙이 커버하는 폭

- 내부도구형, data-heavy UI
- 고객-facing form / route / validation flow
- 발표용 문서와 실제 캡처 기반 demo narrative

## 워크스페이스 명령

```bash
cd study
npm run dev:portfolio
npm run verify:portfolio
```

`dev:portfolio`는 기본적으로 `01-ops-triage-console`을 연다. `verify:portfolio`는 두 앱을 모두 검증한다.
