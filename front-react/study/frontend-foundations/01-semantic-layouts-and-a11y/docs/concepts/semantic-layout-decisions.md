# Semantic Layout Decisions

이 프로젝트는 첫 단계부터 시각 밀도보다 의미 구조를 먼저 고정한다. 그래서 `header`, `nav`, `main`, `aside`를 명시적으로 나누고, settings shell의 핵심 질문도 "예쁜가"가 아니라 "역할이 드러나는가"로 잡았다.

핵심 판단은 세 가지다.

- settings/dashboard shell을 택했다.
  - marketing page보다 form, landmark, status message를 한 화면에서 더 자연스럽게 검증할 수 있다.
- responsive 기준을 "컬럼 수"가 아니라 "reading order 보존"으로 잡았다.
  - 좁은 뷰포트에서 `main`이 먼저 오고, 보조 카드가 뒤로 가게 배치했다.
- 시각적 강조보다 포커스 가시성을 우선했다.
  - keyboard-only 사용자가 현재 위치를 잃지 않도록 `focus-visible` 스타일을 먼저 고정했다.

이 단계에서 일부러 하지 않은 것도 있다.

- 라우팅을 넣지 않았다.
- persistence를 넣지 않았다.
- custom select나 toggle을 만들지 않았다.

이 제한 덕분에 다음 단계에서 DOM state와 event orchestration을 더 선명하게 다룰 수 있다.
