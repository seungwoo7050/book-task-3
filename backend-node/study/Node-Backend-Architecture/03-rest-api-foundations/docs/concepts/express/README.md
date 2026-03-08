# Documentation — Express REST API Architecture

- 상위 리포트: [../../lab-report.md](../../lab-report.md)
- 챕터 개요: [../../README.md](../../README.md)

## 목적

Express 기반 REST API의 계층 분리와 수동 DI를 학습하고, 테스트 가능 구조를 확보한다.
근거: [문서] ../../README.md

## 읽기 순서

1. [express-fundamentals.md](express-fundamentals.md)
2. [layered-architecture.md](layered-architecture.md)
3. [dependency-injection.md](dependency-injection.md)
4. [testing-patterns.md](testing-patterns.md)

근거: [문서] 위 문서군

## 예상 소요시간

- 총 70~90분
- 이론 45분 + 테스트 패턴 25분
근거: [추론] 문서 분량 기반 추정

## 선수지식

- Node.js/Express 기본 라우팅
- TypeScript 클래스/인터페이스
- HTTP 상태코드
근거: [문서] express-fundamentals.md

## 핵심 질문

- 수동 DI가 테스트 격리에 주는 이점은 무엇인가?
- Controller와 Service의 경계는 어디까지인가?
- E2E와 unit 테스트를 어떻게 분리할 것인가?
근거: [문서] layered-architecture.md, [문서] testing-patterns.md
