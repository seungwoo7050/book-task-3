# Legacy Intent Audit

## 결론

기존 레포의 방향성은 설명회에서 제시된 2번 과제와 대체로 맞다.
핵심 요구는 `rule`이 요약하듯 다음 세 가지였다.

1. 상담 품질 정의와 점수화 기준 수립
2. 자동 평가 체계 구성
3. 모니터링 가시화

기존 `legacy/` 구현은 `rubric -> claim/evidence -> judge/score merge -> dashboard` 흐름을 중심으로 설계되어 있어
과제 선택 자체가 잘못되었다고 보기는 어렵다.

## 근거

- 설명회 STT의 2번 과제 요지는 상담사/챗봇의 답변 편차를 줄이기 위한 품질 관리 체계였다.
- `rule`은 품질 정의, 자동 평가, 품질 가시화를 명시했고, 프롬프트/KB/RAG 개선은 선택 구현으로 낮췄다.
- 기존 문서와 코드도 다음 축에 집중했다.
  - 품질 rubric과 failure taxonomy
  - claim extraction과 evidence verification
  - rule/guardrail + LLM judge + score merge
  - golden set replay와 dashboard

## 기존 결과물의 문제

방향은 맞지만 canonical 학습 레포로 쓰기에는 네 가지 문제가 있었다.

1. 과제 선택 근거가 레포 전면에 없다.
2. QA Ops 계층보다 챗봇 런타임 구현이 목표처럼 보이는 지점이 있다.
3. 캐시, 가상환경, `node_modules`, 로컬 DB 같은 생성물이 섞여 있다.
4. 일부 런타임 헬스체크가 heuristic 모드에서도 불필요한 의존성을 건드려 테스트 안정성이 떨어진다.

## 새 기준

새 레포에서는 다음을 canonical 규칙으로 둔다.

- `legacy/`는 원본 증거와 이전 시도 보관소다.
- `study2/`는 2번 과제를 제출 가능한 데모로 만드는 활성 트랙이다.
- `study1/`, `study3/`도 같은 품질 기준으로 미리 설계한다.
- 최종 capstone은 항상 제출 가능한 초기 데모부터 시작하고, 이후 확장 버전은 폴더 복제 방식으로 누적한다.
