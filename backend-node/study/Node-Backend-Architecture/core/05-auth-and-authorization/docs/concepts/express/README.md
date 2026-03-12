# Documentation — Express Auth Guards

- 상위 리포트: [../../lab-report.md](../../lab-report.md)
- 챕터 개요: [../../README.md](../../README.md)

## 목적

JWT 인증/인가를 Express 미들웨어 체인으로 구현할 때의 경계와 보안 규칙을 정리한다.
근거: [문서] ../../README.md

## 읽기 순서

1. [jwt-fundamentals.md](jwt-fundamentals.md)
2. [password-security.md](password-security.md)
3. [middleware-chains.md](middleware-chains.md)
4. [reproducibility.md](reproducibility.md)

근거: [문서] 위 문서군

## 예상 소요시간

- 총 75~95분
- 인증 이론 30분 + 체인/보안 45분
근거: [추론] 문서 분량 기반 추정

## 선수지식

- HTTP Authorization 헤더
- JWT 기본 구조
- 미들웨어 실행 순서
근거: [문서] jwt-fundamentals.md, [문서] middleware-chains.md

## 핵심 질문

- 401과 403의 경계를 체인에서 어떻게 보장하는가?
- 비밀번호 평문 유출을 문서/코드 레벨에서 어떻게 차단하는가?
- 테스트에서 토큰 발급/재사용 흐름을 어떻게 재현하는가?
근거: [문서] middleware-chains.md, [문서] password-security.md, [문서] reproducibility.md
