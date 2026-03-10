# Domain Fixtures — 왜 "재현 가능한 입력"부터 만들었는가

## 출발점

상담 품질을 평가하려면, 먼저 **평가할 대상**이 있어야 한다.
"환불은 몇일 걸려요?"라는 질문에 챗봇이 어떤 답변을 했고, 그 답변이 어떤 문서를 근거로 했는지 — 이 입력이 매번 같아야 비교가 의미 있다.

처음에는 "테스트 코드 안에 하드코딩하면 되지 않나"라고 생각했다. 테스트 파일에 `user_message = "환불은 몇일 걸려요?"`를 직접 쓰면 간단하니까.
하지만 stage 06에서 golden set을 만들고, stage 07에서 dashboard에 replay 결과를 보여줘야 할 때, **같은 입력 데이터를 세 곳에서 복사해야** 한다는 문제가 생겼다.

## 이 단계가 해결하려는 것

핵심 질문:

> "fixture와 replay를 어떻게 분리해야 회귀 테스트와 golden set 생성이 흔들리지 않는가?"

답은 **fixture 파일을 코드에서 분리**하는 것이었다.

- **Knowledge base**: `data/knowledge_base/` 아래 Markdown 파일로. 환불 정책, 본인확인 절차, 해지 정책 등.
- **Replay 세션**: `data/replay_sessions.json`으로. 사용자 질문과 기대되는 근거 문서.
- **Harness**: `src/stage02/harness.py`로. fixture를 읽어서 deterministic하게 검색과 재생을 수행.

## 성공 기준

1. 같은 replay 입력에 대해 항상 같은 retrieved doc order가 나온다.
2. fixture 파일과 harness 코드가 분리되어 수정 범위가 명확하다.
3. 후속 golden set과 version compare 입력으로 이어질 수 있다.

## 이 트랙을 처음 보는 사람을 위한 전제

- 이 stage의 retrieval은 **keyword 수준**이다. 실제 capstone의 retrieval 품질을 대변하지 않는다.
- 목표는 search quality가 아니라 **재현 가능한 입력/출력 contract**이다.
- 평가기가 답변 품질만 보지 않고 **어떤 지식을 인용했는지**도 확인해야 한다는 점이 이 stage의 전제다.
