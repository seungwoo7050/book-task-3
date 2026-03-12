# Docs — Platform Capstone

- 상위 리포트: [../lab-report.md](../lab-report.md)
- 챕터 개요: [../README.md](../README.md)
- 루트 인덱스: [../../learning-index.md](../../learning-index.md)

## 목적

01~05 챕터에서 정의한 아키텍처 규약을 단일 NestJS 애플리케이션에서 통합/검증한다.
근거: [문서] ../README.md

## 읽기 순서

1. [integration-architecture.md](integration-architecture.md)
2. [security-patterns.md](security-patterns.md)
3. [testing-patterns.md](testing-patterns.md)
4. [reproducibility.md](reproducibility.md)

근거: [문서] 위 문서군

## 예상 소요시간

- 총 100~130분
근거: [추론] 문서 분량 기반 추정

## 선수지식

- NestJS 모듈 설계
- JWT/RBAC
- TypeORM + 이벤트 시스템
근거: [문서] integration-architecture.md, [문서] security-patterns.md

## 핵심 질문

- 챕터별 패턴 충돌 없이 단일 파이프라인으로 통합되는가?
- 인증/인가/검증/DB/이벤트의 우선순위와 경계는 일관적인가?
- 테스트 문서가 실제 실행 구조(`data.token`, `:memory:`)와 일치하는가?
근거: [문서] testing-patterns.md, [문서] reproducibility.md
