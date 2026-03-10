# msglab

`msglab`은 네트워크 I/O와 parser 책임을 분리해서 보는 lab이다. 서버를 계속 붙잡고 보기 전에, 줄 경계와 토큰 해석이 어떻게 분리돼야 테스트하기 쉬워지는지 먼저 익힌다.

## 이 프로젝트가 가르치는 것

- IRC line framing과 trailing parameter 규칙
- prefix, command, params를 분해하는 데이터 모델
- validator를 parser와 executor 사이 어디에 둘지 판단하는 방법

## 현재 범위

- 포함: line split, command 정규화, nickname/channel validation, transcript 테스트
- 제외: socket I/O, 실제 IRC session state, room broadcast

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [cpp/README.md](cpp/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 포트폴리오로 확장할 때 보여 줄 것

- 입력 정규화와 유효성 검사를 네트워크 코드와 분리한 이유
- [cpp/tests/test_parser.cpp](cpp/tests/test_parser.cpp) 같은 transcript 테스트 전략
- parser 단계와 executor 단계의 책임 경계를 문서로 설명한 흔적
