# Runtime Demo Presentation

## 5 Minute Flow

1. shared runtime consumer 구조를 먼저 보여 준다.
2. search input에 `metrics`를 입력하고 debounce 뒤 결과가 줄어드는 장면을 보여 준다.
3. query를 지운 뒤 `Load more results`를 눌러 visible window와 metrics panel이 같이 갱신되는 장면을 보여 준다.
4. metrics panel을 가리키며 이 값이 "production profiler"가 아니라 학습용 관찰값임을 설명한다.
5. limitation note로 넘어가 이 demo가 portfolio 앱이 아니라 internals capstone임을 정리한다.

## Talk Track

- "이 앱의 포인트는 UI polish가 아니라 shared runtime을 실제 consumer 구조로 끝까지 연결했다는 데 있다."
- "검색과 pagination은 작지만 state, effect, delegated event, patch commit이 전부 지나가는 시나리오다."
- "metrics panel은 runtime의 한계를 숨기지 않기 위한 장치다."
