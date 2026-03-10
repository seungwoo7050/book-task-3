# 문제 프레이밍

## 학습 목표

이 랩의 질문은 단순하다. 사용자 정보를 매번 DB join으로 해결하지 않고도, access token claims만으로 워크스페이스 생성 같은 첫 도메인 동작을 설명할 수 있는가. 이를 위해 인증과 워크스페이스를 서비스 단위로 나누고, cross-DB 조회를 금지한다.

## 왜 중요한가

- 모놀리식 구조에서는 `users` 테이블을 아무 곳에서나 읽어도 당장 기능은 돌아간다.
- 하지만 서비스를 분리하면 “사용자 정보를 어디서 읽을 것인가”가 바로 경계 설계 문제로 바뀐다.
- 이 문제를 해결하지 못하면 서비스 분리는 디렉터리만 늘어난 복사본에 그친다.

## 선수 지식

- `labs/A-auth-lab`의 로그인과 토큰 발급 흐름
- `labs/C-authorization-lab`의 역할과 권한 확인 방식
- FastAPI dependency injection과 SQLAlchemy 세션 기본

## 성공 기준

- `identity-service`가 발급한 토큰으로 `workspace-service`의 `/internal/workspaces` 호출이 성공해야 한다.
- `workspace-service`는 `identity-service` 데이터베이스를 직접 조회하지 않아야 한다.
- 사용자 정보 전달 규칙이 문서와 테스트에 함께 드러나야 한다.

## 일부러 제외한 범위

- gateway, cookie, CSRF
- Redis Streams와 비동기 이벤트 전달
- tracing, metrics, 운영 문서

## 이 랩이 답하려는 질문

- 최소한의 claim 집합은 무엇인가
- 서비스 분리 첫 단계에서 shared ORM 모델을 왜 끊어야 하는가
- DB ownership을 어기지 않고도 도메인 기능을 유지할 수 있는가

이 랩은 “MSA의 시작점”을 다룬다. 이벤트 브로커나 gateway보다 먼저, 데이터 ownership과 claim 계약을 고정해야 다음 랩들이 의미를 갖는다.
