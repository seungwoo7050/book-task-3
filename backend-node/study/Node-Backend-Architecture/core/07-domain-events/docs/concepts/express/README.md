# Documentation — Express Event System

- 상위 리포트: [../../lab-report.md](../../lab-report.md)
- 챕터 개요: [../../README.md](../../README.md)

## 목적

Node.js EventEmitter 기반 이벤트 설계를 통해 서비스 부수효과를 분리하고 테스트 가능하게 만든다.
근거: [문서] ../../README.md

## 읽기 순서

1. [event-driven-architecture.md](event-driven-architecture.md)
2. [node-eventemitter.md](node-eventemitter.md)
3. [testing-patterns.md](testing-patterns.md)
4. [reproducibility.md](reproducibility.md)

근거: [문서] 위 문서군

## 예상 소요시간

- 총 70~90분
근거: [추론] 문서 분량 기반 추정

## 선수지식

- Observer 패턴
- TypeScript 제네릭
- 이벤트 기반 테스트
근거: [문서] event-driven-architecture.md, [문서] testing-patterns.md

## 핵심 질문

- 이벤트 발행 시점을 성공 경로로 제한하려면?
- 리스너 오류를 메인 트랜잭션에서 어떻게 격리할 것인가?
- 테스트에서 이벤트 전파를 어떤 방식으로 관찰할 것인가?
근거: [문서] node-eventemitter.md, [문서] testing-patterns.md
