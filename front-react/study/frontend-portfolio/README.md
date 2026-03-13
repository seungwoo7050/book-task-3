# Frontend Portfolio

이 트랙은 채용용으로 설명 가능한 제품형 결과물을 만드는 단계다. 내부도구형 UI, 고객-facing UI, 실시간 협업 UI를 각각 다른 프로젝트로 두어 서로 다른 프론트 문제를 어떻게 푸는지 보여 준다.

## 프로젝트 인덱스

| 프로젝트 | 문제 질문 | 내가 만든 답 | 검증 | 다음 단계 |
| --- | --- | --- | --- | --- |
| [01-ops-triage-console](01-ops-triage-console/README.md)<br>[problem](01-ops-triage-console/problem/README.md) · [next](01-ops-triage-console/next/README.md) · [docs](01-ops-triage-console/docs/README.md) | 데이터가 많은 운영 화면에서 triage workflow를 어떻게 설계하고 검증하는가 | dashboard, queue, saved view, bulk action, optimistic update를 갖춘 Next.js 운영 콘솔 | `verify --workspace @front-react/ops-triage-console`<br>`typecheck` + `vitest` + `playwright` | 고객-facing multi-step flow를 보여 주는 프로젝트로 이동 |
| [02-client-onboarding-portal](02-client-onboarding-portal/README.md)<br>[problem](02-client-onboarding-portal/problem/README.md) · [next](02-client-onboarding-portal/next/README.md) · [docs](02-client-onboarding-portal/docs/README.md) | 고객-facing onboarding flow에서 validation, draft, route guard를 어떻게 묶는가 | sign-in, wizard, workspace setup, invite, submit retry를 갖춘 Next.js 포털 | `verify --workspace @front-react/client-onboarding-portal`<br>`typecheck` + `vitest` + `playwright` | 협업 상태를 설명하는 capstone으로 이동 |
| [03-realtime-collab-workspace](03-realtime-collab-workspace/README.md)<br>[problem](03-realtime-collab-workspace/problem/README.md) · [next](03-realtime-collab-workspace/next/README.md) · [docs](03-realtime-collab-workspace/docs/README.md) | 실시간 협업 UI에서 optimistic patch, reconnect replay, conflict surface를 어떻게 설명 가능하게 만들 것인가 | shared board, doc blocks, presence, conflict banner를 갖춘 Next.js 협업 워크스페이스 | `verify --workspace @front-react/realtime-collab-workspace`<br>`typecheck` + `vitest` + `playwright` | 포트폴리오 트랙의 최종 capstone으로 발표 품질까지 정리한다 |

## 워크스페이스 명령

```bash
cd study
npm run dev:portfolio
npm run verify:portfolio
```

`dev:portfolio`는 기본적으로 `01-ops-triage-console`을 연다. 개별 앱 실행과 검증은 각 프로젝트 README의 workspace 명령을 따른다.
