# J-edge-gateway-lab 설계 문서

이 폴더는 J-edge-gateway-lab의 설계 설명을 모아 둔 곳입니다. 실행 순서보다 왜 이런 경계를 택했고 무엇을 설명해야 하는지를 먼저 정리합니다.

## 이 문서에서 먼저 볼 질문

- 왜 public API를 gateway가 유지해야 하는가
- 왜 쿠키와 CSRF를 내부 서비스에 넘기지 않는가
- request id는 어떤 경로로 전파되는가
- upstream 오류는 어디서 어떤 HTTP 상태로 번역해야 하는가

## 이 문서에서 중심으로 보는 구조

- 브라우저는 gateway만 호출한다.
- gateway는 public route shape를 유지한 채 내부 `identity-service`, `workspace-service`, `notification-service`로 fan-out 한다.
- cookie와 CSRF는 gateway에만 남고, 내부 서비스는 bearer token만 읽는다.
- request id는 gateway에서 생성해 모든 내부 호출로 전달한다.

## 읽고 나면 설명할 수 있어야 하는 것

- edge와 internal service의 책임 차이
- gateway fan-out과 upstream 오류 표면화 방식
- 브라우저 상태와 서비스 간 계약의 분리
- J 랩이 왜 “새 기능 추가”보다 “경계 재설계”에 가까운지

## 역할이 다른 관련 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [학습 노트](../notion/README.md)
