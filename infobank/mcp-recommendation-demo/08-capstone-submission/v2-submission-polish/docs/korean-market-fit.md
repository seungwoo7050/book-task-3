# 한국어 시장 적합성

`v2-submission-polish`는 최종 제출 버전이므로, 추천 결과가 "동작한다"는 사실만이 아니라 한국어 운영자가 바로 읽고 설명할 수 있다는 점까지 증빙해야 한다. 이 문서는 한국어 중심 사용성이 어떤 설계 요소로 보장되는지 요약한다.

## 왜 중요한가

- 추천 근거가 영어-only면 발표 시연에서는 통과하더라도 실제 팀 문서나 운영 설명으로 옮기기 어렵다.
- catalog가 한국어 업무 시나리오를 반영하지 않으면 offline eval이 좋아 보여도 현업 질의와 맞지 않을 수 있다.
- release artifact가 한국어로 정리돼 있어야 학생이 자기 포트폴리오 문서로 그대로 재사용하기 쉽다.

## v2에서 어떻게 반영했는가

- recommendation explanation은 한국어 템플릿으로 생성되며, 선택 이유와 주의점이 한국어 문장으로 노출된다.
- catalog seed는 사내 위키 검색, 릴리즈 점검, incident review, 운영 도구 추천 같은 한국어 질의를 기본 시나리오로 사용한다.
- compatibility gate는 summary, use case, differentiation, exposure 메타데이터가 한국어로 비어 있지 않은지 함께 검사한다.
- release gate와 artifact export는 운영자 설명용 Markdown을 만들어 제출 증빙과 팀 문서화 흐름을 연결한다.
- dashboard copy도 운영자가 바로 읽을 수 있는 한국어 문구를 기본값으로 둔다.

## 검증 경로

- `pnpm eval`: 한국어 seeded query가 top-3 recall과 explanation completeness 기준을 만족하는지 확인한다.
- `pnpm compatibility rc-release-check-bot-1-5-0`: 한국어 메타데이터 완전성이 gate에 포함되는지 확인한다.
- `pnpm release:gate rc-release-check-bot-1-5-0`: 제출용 artifact에 한국어 설명, 검증, 리스크 문단이 모두 포함되는지 확인한다.
