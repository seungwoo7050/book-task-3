# 회고

## 이번 랩에서 얻은 것

- gateway가 단순 프록시가 아니라 public contract를 보존하는 별도 책임이라는 점이 분명해졌다.
- 쿠키/CSRF를 edge에만 두면 내부 서비스는 훨씬 단순한 bearer 계약만 유지하면 된다.
- request id 전파와 오류 번역도 gateway가 있어야 비로소 설명 가능한 기능이 된다.

## 이번 랩의 약점

- gateway가 생기면서 로컬 통합 테스트가 무거워진다.
- timeout, 재시도, websocket fan-out, edge auth 정책이 새로 추가돼 코드량이 늘어난다.
- 아직 분산 tracing backend는 없어서 request id가 로그 correlation의 최소선에 머문다.

## 다음 랩으로 넘기는 질문

- 서비스별 live/ready는 무엇을 확인해야 하는가
- 운영 문서는 어디까지 사실이고 어디부터 가정인지 어떻게 구분할 것인가
- gateway를 포함한 다중 서비스 구조에서 “운영 가능성”을 최소한 어떻게 증명할 것인가
