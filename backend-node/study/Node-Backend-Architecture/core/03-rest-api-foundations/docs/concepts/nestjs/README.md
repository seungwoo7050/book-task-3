# Documentation — NestJS REST API Architecture

- 상위 리포트: [../../lab-report.md](../../lab-report.md)
- 챕터 개요: [../../README.md](../../README.md)

## 목적

NestJS 모듈/데코레이터/DI 컨테이너가 Express 수동 패턴을 어떻게 추상화하는지 이해한다.
근거: [문서] ../../README.md, [문서] express-vs-nestjs.md

## 읽기 순서

1. [nestjs-fundamentals.md](nestjs-fundamentals.md)
2. [decorators-and-metadata.md](decorators-and-metadata.md)
3. [express-vs-nestjs.md](express-vs-nestjs.md)
4. [testing-patterns.md](testing-patterns.md)

근거: [문서] 위 문서군

## 예상 소요시간

- 총 80~100분
- 프레임워크 개념 55분 + 테스트 25분
근거: [추론] 문서 분량 기반 추정

## 선수지식

- TypeScript 데코레이터 기초
- DI 개념(생성자 주입)
- Express 기본 이해(비교 목적)
근거: [문서] decorators-and-metadata.md, [문서] express-vs-nestjs.md

## 핵심 질문

- NestJS에서 `@Controller/@Injectable`은 어떤 런타임 동작을 유도하는가?
- Express의 수동 조립 대비 어떤 유지보수 이점이 있는가?
- TestingModule은 어떤 문제를 해결하는가?
근거: [문서] nestjs-fundamentals.md, [문서] testing-patterns.md
