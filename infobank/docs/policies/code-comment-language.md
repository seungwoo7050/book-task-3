# Code Comment Language Policy

이 레포의 설명용 코드 주석과 docstring은 한국어 우선으로 유지한다.

## 규칙

- Python, TS, TSX, JS, JSX의 authored explanatory comment와 docstring은 한국어로 쓴다.
- 식별자, 패키지명, 함수명, CLI 명령, env var, pragma, lint directive, protocol/library 이름은 영어 그대로 둔다.
- 설명 가치가 거의 없는 주석은 번역하지 않고 삭제한다.
- package `__init__` 같은 짧은 docstring도 한국어로 바꾸되 의미만 옮기고 동작은 건드리지 않는다.
- generated artifact, vendored source, build output은 이 정책 대상이 아니다.
