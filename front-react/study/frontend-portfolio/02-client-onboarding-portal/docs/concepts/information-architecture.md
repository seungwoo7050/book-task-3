# Information Architecture

`Client Onboarding Portal`은 두 route와 세 step으로 구조를 나눈다.

## Routes

- `/`: sign-in entry
- `/onboarding?step=workspace|invites|review`: protected onboarding flow
- `/case-study`: hiring review narrative

## Step Responsibilities

- `workspace`
  - workspace name, industry, region, team size, compliance owner
  - draft save의 기준이 되는 기본 정보
- `invites`
  - 첫 collaborator 초대
  - submit readiness를 위해 최소 한 명의 teammate 확보
- `review`
  - summary 확인
  - checklist completion
  - submit failure / retry handling
