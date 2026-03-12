# Documentation — NestJS Pipeline

- 상위 리포트: [../../lab-report.md](../../lab-report.md)
- 챕터 개요: [../../README.md](../../README.md)

## 목적

Pipe/Filter/Interceptor를 조합해 NestJS 요청 처리 파이프라인을 표준화한다.
근거: [문서] ../../README.md

## 읽기 순서

1. [pipes-and-validation.md](pipes-and-validation.md)
2. [exception-filters.md](exception-filters.md)
3. [interceptors.md](interceptors.md)
4. [reproducibility.md](reproducibility.md)

근거: [문서] 위 문서군

## 예상 소요시간

- 총 75~95분
근거: [추론] 문서 분량 기반 추정

## 선수지식

- NestJS lifecycle 개요
- class-validator 기본
- RxJS 기초(`map`, `tap`)
근거: [문서] pipes-and-validation.md, [문서] interceptors.md

## 핵심 질문

- 전역/로컬 파이프라인 설정의 우선순위는?
- ExceptionFilter는 어떤 에러를 어디서 변환해야 하는가?
- Interceptor가 응답 계약을 표준화하는 가장 안전한 방식은?
근거: [문서] exception-filters.md, [문서] interceptors.md
