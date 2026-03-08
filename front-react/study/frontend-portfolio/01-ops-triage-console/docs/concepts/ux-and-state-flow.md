# UX 와 상태 흐름

## 화면 구조

- 상단: 제품 제목, queue health, demo controls
- 좌측 메인: filters + saved views + triage queue
- 우측 보조: 선택된 이슈 상세와 triage form
- 별도 라우트: `/case-study`

## 상태 흐름

1. queue query가 현재 filter와 saved view 기준으로 목록을 가져온다
2. row를 선택하면 detail query가 해당 이슈를 불러온다
3. triage action은 먼저 UI를 optimistic하게 갱신한다
4. 요청이 실패하면 rollback하고 retry action을 제공한다
5. 요청이 성공하면 undo toast를 보여 주고 summary와 detail을 재동기화한다

## 왜 이 구조인가

- 운영자는 목록과 상세를 빠르게 오가야 하므로 split view가 효율적이다
- bulk action은 queue 문맥 안에서 처리해야 하므로 table selection과 바로 붙어 있어야 한다
- saved view는 반복적인 triage 작업을 줄이는 핵심 도구다

