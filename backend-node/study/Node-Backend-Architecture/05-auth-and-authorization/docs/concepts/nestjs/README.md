# Documentation — NestJS Auth Guards

- 상위 리포트: [../../lab-report.md](../../lab-report.md)
- 챕터 개요: [../../README.md](../../README.md)

## 목적

Passport JWT Strategy와 Guard/Reflector 기반 RBAC를 NestJS 방식으로 체계화한다.
근거: [문서] ../../README.md

## 읽기 순서

1. [passport-jwt.md](passport-jwt.md)
2. [nestjs-guards.md](nestjs-guards.md)

근거: [문서] 위 문서군

## 예상 소요시간

- 총 55~75분
근거: [추론] 문서 분량 기반 추정

## 선수지식

- NestJS 모듈/가드 개념
- JWT payload 구조
근거: [문서] passport-jwt.md, [문서] nestjs-guards.md

## 핵심 질문

- Strategy와 Guard의 책임 경계는 무엇인가?
- Reflector는 role 메타데이터를 어떻게 읽는가?
- Express 체인 대비 선언형 보안의 장단점은 무엇인가?
근거: [문서] nestjs-guards.md
