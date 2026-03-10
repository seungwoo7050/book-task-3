# J-edge-gateway-lab 노트 안내

이 노트는 J 랩을 “public API를 유지한 채 내부를 분리하려면 무엇을 edge에 남겨야 하는가”라는 질문으로 읽게 만드는 보조 문서다.

## 추천 읽기 순서

1. `00-problem-framing.md`: 왜 gateway가 필요한지 큰 그림을 본다.
2. `01-approach-log.md`: 왜 cookie/CSRF를 edge에만 남겼는지 본다.
3. `05-development-timeline.md`: 실제 검증 순서를 따라간다.
4. `02-debug-log.md`: gateway가 생기면서 어떤 실패가 새로 생겼는지 확인한다.
5. `03-retrospective.md`, `04-knowledge-index.md`: 운영성 랩으로 넘어갈 질문과 재사용 개념을 정리한다.
