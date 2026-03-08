# Documentation — NestJS Event System

- 상위 리포트: [../../lab-report.md](../../lab-report.md)
- 챕터 개요: [../../README.md](../../README.md)

## 목적

`@nestjs/event-emitter` + `@OnEvent` 기반 도메인 이벤트 설계와 검증 전략을 정리한다.
근거: [문서] ../../README.md

## 읽기 순서

1. [domain-events.md](domain-events.md)
2. [nestjs-event-emitter.md](nestjs-event-emitter.md)
3. [testing-patterns.md](testing-patterns.md)

근거: [문서] 위 문서군

## 예상 소요시간

- 총 60~80분
근거: [추론] 문서 분량 기반 추정

## 선수지식

- NestJS provider/DI
- 이벤트 기반 아키텍처 기초
근거: [문서] domain-events.md

## 핵심 질문

- 이벤트 클래스 설계가 테스트 가독성에 어떤 영향을 주는가?
- `on/off` 정리 정책은 어떻게 운영할 것인가?
- E2E에서 실제 리스너 실행을 어떻게 확인할 것인가?
근거: [문서] testing-patterns.md
