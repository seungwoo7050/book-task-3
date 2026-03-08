# Core Concepts

## 핵심 개념

- table-driven test는 입력과 기대값을 나란히 놓아 케이스 확장을 쉽게 만든다.
- subtest는 실패 지점을 이름으로 드러내 준다.
- benchmark는 “더 빠르다”는 감각을 숫자로 바꾸는 최소 도구다.
- `sync.Mutex`로 감싼 recorder는 race detector를 통과시키는 가장 단순한 구조다.

## Trade-offs

- 테스트 테이블이 커지면 가독성이 떨어질 수 있다.
- benchmark 수치만 보고 설계를 바꾸면 실제 서비스 병목과 어긋날 수 있다.

## 실패하기 쉬운 지점

- race-safe snapshot을 만들지 않으면 테스트는 통과해도 실제 읽기 경합이 남는다.
- 파싱 에러를 너무 넓게 뭉개면 디버깅 신호가 약해진다.

