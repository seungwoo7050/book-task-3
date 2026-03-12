# 04 SQL And Data Modeling

## 한 줄 요약

스키마 설계, join, transaction을 게임 상점 예제로 묶어 SQL 기초를 백엔드 문맥에서 익히는 브리지 과제다.

## 이 프로젝트가 푸는 문제

- 스키마 설계와 관계 모델링을 실제 도메인 예제로 익혀야 한다.
- PK/FK, unique constraint, index가 어떤 제약을 표현하는지 손으로 확인해야 한다.
- join query와 transaction 기초를 구매 흐름으로 설명해야 한다.

## 내가 만든 답

- `players`, `items`, `inventory`를 중심으로 한 게임 상점 스키마와 조회/구매 예제를 `solution/go`에 구현했다.
- in-memory SQLite로 스키마 부트스트랩과 join query를 바로 실행할 수 있게 했다.
- 다음 단계 저장소 API 과제로 이어지도록 도메인과 쿼리 예제를 분리했다.

## 핵심 설계 선택

- ORM 없이 SQL 구조를 먼저 보여 주기 위해 스키마와 쿼리 자체를 학습 표면에 올렸다.
- 실제 migration tool은 뒤로 미루고 데이터 모델과 transaction 경계를 먼저 학습하게 했다.

## 검증

- `cd solution/go && go run ./cmd/schemawalk`
- `cd solution/go && go test ./...`

## 제외 범위

- 외부 DB 운영
- migration binary 적용

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: `study`에서 새로 추가한 브리지 과제
