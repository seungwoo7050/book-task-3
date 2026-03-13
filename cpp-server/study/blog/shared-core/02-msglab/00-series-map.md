# msglab series map

`msglab`은 서버를 띄우는 문서가 아니다. 대신 뒤의 모든 lab이 공통으로 기대는 입력 표면을 먼저 고정한다. 그래서 시리즈도 "한 줄을 구조화하는 방법 -> 그 줄을 검증하는 방법 -> 그 표면이 실제로 충분한지 확인하는 방법" 순서로 읽히게 나눴다.

첫 글은 `Message` 모델과 line framing을 붙잡는다. 둘째 글은 정규화와 validation helper가 왜 parser 근처에 있어야 하는지 설명한다. 마지막 글은 transcript 스타일 테스트가 IRC와 game command 양쪽을 어디까지 보호하는지, 그리고 여전히 서버 레이어가 맡아야 할 일은 무엇인지 정리한다.

## 글 순서

1. [10-message-model-and-framing.md](10-message-model-and-framing.md)
2. [20-validation-and-command-normalization.md](20-validation-and-command-normalization.md)
3. [30-transcript-coverage-and-boundaries.md](30-transcript-coverage-and-boundaries.md)

