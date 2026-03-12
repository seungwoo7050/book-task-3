# Node HTTP 구현

## 담당 범위

Node 기본 `http` 모듈 기반으로 요청/응답 계약을 직접 다루는 단일 구현 레인이다.

## 현재 구조

- `src/`: 서버, 라우팅, body parsing 유틸리티
- `tests/`: HTTP 계약 검증

## 실행과 검증

- install: `pnpm install`
- build: `pnpm run build`
- test: `pnpm run test`
- server: `pnpm start`

## 이 레인을 볼 때 기준

- 이 레인의 상위 문제 요약은 [../README.md](../README.md)에서 본다.
- canonical problem statement는 [../problem/README.md](../problem/README.md)에서 확인한다.
- 개념 문서 인덱스는 [../docs/README.md](../docs/README.md), 장문 학습 로그 인덱스는 [../notion/README.md](../notion/README.md)에 있다.
