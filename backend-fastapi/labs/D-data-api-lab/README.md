# D-data-api-lab

데이터 중심 백엔드 API를 어떻게 구조화할지 연습하는 랩입니다. CRUD 자체보다도 필터링, 정렬, 소프트 삭제, 낙관적 락처럼 시간이 지나도 설명 가치가 남는 설계 포인트에 집중합니다.

## 이 랩에서 배우는 것

- 프로젝트, 태스크, 댓글 API 설계
- 서비스 계층과 ORM 경계 정리
- 필터링, 정렬, 페이지 기반 페이지네이션
- 소프트 삭제
- optimistic locking

## 선수 지식

- SQLAlchemy 기본 모델링
- REST API와 상태 코드 기본
- 트랜잭션과 동시성의 기초 개념

## 구현 범위

- projects / tasks / comments CRUD
- 목록 조회용 query parameter
- 버전 필드 기반 충돌 감지
- health endpoint

## 일부러 단순화한 점

- 인증/인가를 붙이지 않고 데이터 경계에 집중합니다.
- 페이지네이션은 cursor 대신 page-based 모델로 유지합니다.

## 실행 방법

1. [problem/README.md](problem/README.md)에서 요구되는 데이터 조작 범위를 읽습니다.
2. [fastapi/README.md](fastapi/README.md)로 워크스페이스를 실행합니다.
3. [docs/README.md](docs/README.md)와 [notion/README.md](notion/README.md)로 데이터 설계 포인트를 정리합니다.

## 검증 방법

- `cd fastapi && make lint`
- `cd fastapi && make test`
- `cd fastapi && make smoke`
- `cd fastapi && docker compose up --build`

## 추천 학습 순서

1. 데이터 모델과 API 범위를 먼저 확인합니다.
2. optimistic locking과 soft delete가 왜 필요한지 문서로 정리합니다.
3. 자신의 제품 도메인에 맞춰 aggregate를 바꾸는 연습을 해 봅니다.

## 포트폴리오로 확장하려면

- cursor pagination, 검색 인덱스, 이벤트 로그 같은 확장 주제를 붙일 수 있습니다.
- 도메인 이벤트나 감사 로그까지 이어 가면 CRUD를 넘는 설명이 가능합니다.
- 포트폴리오 README에는 엔터티 목록보다 "변경 충돌을 어떻게 다뤘는가"를 먼저 적는 편이 좋습니다.
