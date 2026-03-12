# 08 SQL Store API

## 한 줄 요약

SQLite 기반 CRUD API에 migration, optimistic update, transaction rollback을 결합한 백엔드 코어 중심 과제다.

## 이 프로젝트가 푸는 문제

- `database/sql` 기반 CRUD API를 구현해야 한다.
- migration up/down과 repository 계층을 같이 설계해야 한다.
- optimistic update와 transaction rollback을 실제 요청 흐름에 반영해야 한다.

## 내가 만든 답

- 상품 CRUD API와 SQLite 저장소를 `solution/go`에 구현했다.
- migration 파일, repository 계층, optimistic update 경로를 코드와 테스트에 같이 넣었다.
- 재고 부족 같은 실패 케이스에서는 transaction rollback을 명시적으로 검증한다.

## 핵심 설계 선택

- DB 접근은 `database/sql`과 repository 계층으로 감싸 ORM 없이 경계를 드러냈다.
- optimistic update와 rollback을 같은 과제에 묶어 이후 정합성 과제의 발판으로 삼았다.

## 검증

- `cd solution/go && go run ./cmd/server`
- `cd solution/go && go test ./...`

## 제외 범위

- 외부 DB 엔진 운영
- connection pool 튜닝

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: `study`에서 새로 추가한 브리지 과제
