# H-service-boundary-lab 문서 지도

이 문서는 `identity-service`와 `workspace-service`를 처음으로 분리할 때 어떤 경계를 먼저 고정해야 하는지 설명하는 개념 지도다. 여기서 중요한 것은 서비스를 많이 만들었다는 사실이 아니라, 사용자 정보 전달 방식을 `DB join`에서 `token claims`로 바꾸는 기준을 분명히 세우는 일이다.

## 먼저 보면 좋은 질문

- 인증 서비스와 워크스페이스 서비스를 왜 분리하는가
- 어떤 데이터는 claim으로 넘기고 어떤 데이터는 넘기지 않는가
- 서비스별 DB ownership을 어디까지 강제할 것인가
- 공유 ORM 모델을 금지하면 무엇이 불편해지고 무엇이 명확해지는가

## 이 문서에서 중심으로 보는 구조

- `identity-service`는 회원가입, 이메일 검증, 로그인, 토큰 발급만 책임진다.
- `workspace-service`는 워크스페이스 생성 같은 도메인 동작만 책임진다.
- 두 서비스는 서로의 데이터베이스를 직접 읽지 않는다.
- 사용자 정보는 access token claims를 통해서만 전달한다.

## 읽고 나면 설명할 수 있어야 하는 것

- `identity-service`와 `workspace-service`의 책임 경계
- bearer claims가 경계 계약으로 쓰이는 이유
- 공유 ORM 모델을 피하는 이유
- 서비스 분리를 시작할 때 gateway나 event broker를 일부러 뒤로 미루는 이유

## 함께 보면 좋은 문서

- [문제 정의](../problem/README.md)
- [FastAPI 실행 문서](../fastapi/README.md)
- [학습 노트](../notion/README.md)
