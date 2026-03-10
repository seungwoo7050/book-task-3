# MCP Recommendation Demo v3 발표 자료

## 1. 그래서 v3로 뭘 할 수 있나

- 한 팀이 직접 설치해서 로그인된 권한 아래 MCP catalog와 release gate를 운영할 수 있다.
- 추천은 즉시 실행하고, 무거운 검증은 job으로 큐에 넣어 안전하게 돌릴 수 있다.
- 누가 무엇을 바꿨는지 audit log와 artifact로 남길 수 있다.

발표 멘트:
`v2`가 capstone demo였다면, `v3`는 “그래서 남이 설치해서 써도 되나?”라는 질문에 답하는 버전입니다.

## 2. 실제 사용 사례

사용자:

- 플랫폼 팀 owner
- 릴리즈 운영자 operator
- 결과만 보는 viewer

상황:

팀이 `release-check-bot@1.5.0`을 self-hosted 환경에서 운영한다. owner가 접근을 정리하고, operator가 compare와 release gate를 돌린 뒤, viewer가 artifact만 확인한다.

## 3. 시나리오

1. owner가 로그인한다.
2. owner가 `Team Access`에서 계정을 만든다.
3. operator가 bundle import/export와 candidate recommendation을 실행한다.
4. operator가 compare, compatibility, release gate, artifact export를 job으로 등록한다.
5. viewer가 read-only 화면에서 결과와 artifact를 확인한다.

## 4. Login Screen

![v3 login](./presentation-assets/01-login.png)

설명:

- self-hosted 진입점은 로그인부터 시작한다.
- seed 계정이 명시되어 있어서 로컬 데모 재현이 쉽다.

## 5. Owner Dashboard

![v3 owner dashboard](./presentation-assets/02-owner-dashboard.png)

설명:

- owner는 settings, team access, audit log까지 볼 수 있다.
- single-workspace boundary를 콘솔 상단에서 바로 확인할 수 있다.

## 6. Candidate Recommendation

![v3 candidate](./presentation-assets/03-candidate-recommendation.png)

설명:

- 추천 자체는 즉시 실행한다.
- 한국어 explanation으로 operator가 “왜 이 MCP가 맞는지”를 바로 읽을 수 있다.

## 7. Job Activity

![v3 jobs](./presentation-assets/04-job-activity.png)

설명:

- compare, compatibility, release gate, artifact export는 job으로 등록한다.
- 콘솔은 결과를 poll하고 최근 상태를 남긴다.

## 8. Audit Log

![v3 audit](./presentation-assets/05-audit-log.png)

설명:

- owner는 login, CRUD, job enqueue 흔적을 확인할 수 있다.
- 추천 품질뿐 아니라 운영 책임을 추적할 수 있다는 점이 `v3`의 핵심이다.

## 9. Artifact Preview

![v3 artifact](./presentation-assets/06-artifact-preview.png)

설명:

- gate가 끝난 뒤 제출/공유용 Markdown artifact를 바로 확인할 수 있다.
- viewer는 read-only로 이 결과만 확인할 수 있다.

## 10. 검증 결과

- offline eval target: `top3Recall >= 0.90`
- expected seeded result: `top3Recall = 0.9583`
- expected seeded compare uplift: `0.1146`
- compatibility gate: `PASS`
- release gate: `PASS`

## 11. 마무리

한 문장 요약:

`v3`는 MCP 추천 데모를 “한 팀이 직접 설치해서 운영해 볼 수 있는 self-hosted 도구”로 바꾼 버전이다.
