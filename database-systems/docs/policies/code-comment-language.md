# Code Comment Language Policy

이 레포의 설명용 코드 주석과 docstring은 한국어 우선으로 유지합니다.

## 규칙

- 설명용 `//`, `#`, docstring은 한국어로 씁니다.
- 식별자, 패키지명, 함수명, CLI 명령, pragma, protocol/library 이름은 영어 그대로 둡니다.
- 설명 가치가 거의 없는 주석은 번역하지 않고 삭제합니다.
- Go exported comment는 식별자로 시작하는 규칙을 지키면서 한국어로 씁니다. 예: `// SkipList는 ...`
- 테스트 프레임워크용 pragma나 lint directive는 원문을 유지합니다.
