# Information Architecture

`Realtime Collab Workspace`는 화면이 커 보이지만 사실 질문은 단순하다. "지금 누가 있고, 무엇이 바뀌었고, 지금 이 값이 믿을 만한가"를 같은 화면에서 바로 읽게 해야 한다. 그래서 정보 구조를 보드, 문서, presence, activity 네 덩어리로 고정했다.

## 설계 기준

- 편집 surface와 협업 상태를 같은 접힘 없이 보여 준다.
- board와 doc는 같은 patch envelope를 쓰므로 시각 구조도 같은 위계로 둔다.
- conflict는 숨은 토스트가 아니라 상단 배너로 노출한다.
- presence와 activity는 부가 기능이 아니라 신뢰 회복 장치로 취급한다.

## 구조

1. hero/status: viewer, connection, queued patch, conflict count
2. shared board cards: 빠른 짧은 patch surface
3. shared doc blocks: 조금 더 긴 text patch surface
4. presence rail: 현재 collaborators와 상태
5. activity log: local/remote/system 이벤트 시간축

이 배치는 "무엇을 편집하는가"와 "지금 sync가 어떻게 흘렀는가"를 한 번에 설명하게 만든다.
