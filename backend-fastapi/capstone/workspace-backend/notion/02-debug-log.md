# 디버그 로그

## 실패 사례

통합 초기에 일부 모델이 schema bootstrap 대상에서 빠져 membership, invite 같은 테이블이 생성되지 않거나, CSRF / WebSocket 순서 문제로 통합 테스트가 불안정한 일이 있었다.

## 원인

- SQLAlchemy 모델은 import side effect에 의존하므로, bootstrap에서 빠진 모델은 metadata에 등록되지 않는다.
- cookie + CSRF와 WebSocket + HTTP 조합은 테스트에서 실행 순서를 명확히 맞추지 않으면 흔들리기 쉽다.

## 수정

- bootstrap 경로에서 필요한 모델 import를 명시적으로 유지했다.
- CSRF가 필요한 요청은 쿠키와 헤더 순서를 지키도록 테스트를 정리했다.
- WebSocket과 HTTP를 섞는 테스트는 drain과 receive 순서를 고정했다.

## 검증 근거

- 이 실패는 통합 프로젝트에서 모델 import 누락과 테스트 순서 문제가 얼마나 자주 발생하는지 보여 준다.
- 마지막 기록된 검증은 [../../../docs/verification-report.md](../../../docs/verification-report.md)를 따른다.

## 남은 메모

통합 프로젝트에서는 개별 기능 버그보다 "경계 간 순서 충돌"이 더 자주 나타난다.
