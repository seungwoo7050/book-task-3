# Documentation — Express Pipeline

- 상위 리포트: [../../lab-report.md](../../lab-report.md)
- 챕터 개요: [../../README.md](../../README.md)

## 목적

검증/에러/로깅/응답 래핑을 Express 미들웨어 체인으로 일관되게 구성한다.
근거: [문서] ../../README.md

## 읽기 순서

1. [zod-validation.md](zod-validation.md)
2. [error-handling.md](error-handling.md)
3. [logging-patterns.md](logging-patterns.md)
4. [reproducibility.md](reproducibility.md)

근거: [문서] 위 문서군

## 예상 소요시간

- 총 70~90분
근거: [추론] 문서 분량 기반 추정

## 선수지식

- Express 미들웨어 등록 순서
- Zod 스키마 정의
근거: [문서] zod-validation.md

## 핵심 질문

- 검증 실패/시스템 에러를 하나의 응답 규약으로 묶을 수 있는가?
- 로깅과 비즈니스 로직을 어떻게 분리할 것인가?
- 래핑 미들웨어가 기존 응답 계약을 깨지 않게 하려면?
근거: [문서] error-handling.md, [문서] logging-patterns.md
