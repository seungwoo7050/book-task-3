# Core Concepts

## 핵심 개념

- `application` struct에 의존성을 모으면 handler와 middleware를 같은 문맥에서 다루기 쉽다.
- JSON envelope는 응답 shape를 고정해 클라이언트와 테스트를 단순하게 만든다.
- `recoverPanic`, 요청 로깅, CORS 같은 middleware는 프레임워크 없이도 충분히 조합 가능하다.
- graceful shutdown은 SIGINT/SIGTERM 이후 새 요청을 막고 기존 요청을 정리하는 흐름이다.

## Trade-offs

- in-memory store는 문제 범위를 줄여 주지만 실전 DB 오류 처리 감각은 주지 못한다.
- 표준 라이브러리만 쓰면 학습엔 좋지만 반복 코드가 늘어난다.

## 실패하기 쉬운 지점

- validation 오류와 not-found 오류를 같은 응답으로 뭉개면 API 의미가 약해진다.
- middleware 체인 순서를 잘못 두면 panic recovery나 로깅이 기대와 다르게 동작할 수 있다.

