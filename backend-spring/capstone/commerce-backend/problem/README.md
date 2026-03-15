# commerce-backend 문제 정의

개별 Spring 랩에서 학습한 인증, 카탈로그, 장바구니, 주문, 운영 개념을 하나의 커머스 서비스로 다시 조합하는 baseline capstone을 만든다.

## 성공 기준

- 하나의 modular monolith 안에서 커머스 기본 흐름이 연결된다.
- 랩 학습을 통합했을 때 어떤 경계가 남는지 설명할 수 있다.
- 이후 `commerce-backend-v2`가 왜 필요한지 비교 기준이 된다.

## canonical verification 시작 위치

- 실행과 검증 진입점은 [../spring/README.md](../spring/README.md)다.

## 이번 단계에서 다루지 않는 것

- persisted auth의 깊이
- payment 처리
- 완전한 이벤트 연동

이 디렉터리는 baseline capstone의 출제 의도와 범위를 고정하는 곳이다.
