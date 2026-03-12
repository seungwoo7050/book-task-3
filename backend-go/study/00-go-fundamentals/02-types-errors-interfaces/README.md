# 02 Types Errors Interfaces

## 한 줄 요약

struct, method, interface, custom error를 작은 상품 카탈로그로 묶어 타입 감각을 붙이는 과제다.

## 이 프로젝트가 푸는 문제

- struct와 method를 실제 도메인 모델에 적용해야 한다.
- pointer receiver와 interface 분리를 손으로 겪어야 한다.
- custom error와 sentinel error를 구분해 반환해야 한다.

## 내가 만든 답

- 작은 상품 카탈로그와 가격 계산 규칙을 `solution/go`에 구현했다.
- 가격 정책은 interface로 분리하고, SKU 중복과 조회 실패는 명시적 error로 노출한다.
- 도메인 규칙과 출력 포맷을 나눠 타입 시스템을 먼저 익히게 했다.

## 핵심 설계 선택

- 가격 계산 규칙을 interface로 분리해 concrete type과 정책 객체의 경계를 드러냈다.
- 에러는 문자열 비교 대신 sentinel/custom error로 다뤄 이후 HTTP 계층 연결에 대비했다.

## 검증

- `cd solution/go && go run ./cmd/inventorydemo`
- `cd solution/go && go test ./...`

## 제외 범위

- mock 전략 심화
- 외부 저장소 연동

## 읽는 순서

1. [problem/README.md](problem/README.md)에서 canonical 문제 정의와 성공 기준을 읽는다.
2. [solution/README.md](solution/README.md)에서 구현 범위와 검증 진입점을 확인한다.
3. [docs/README.md](docs/README.md)에서 개념 설명과 참고 문서를 따라간다.
4. [notion/README.md](notion/README.md)에서 접근 로그, 디버그 기록, 회고를 확인한다.

## 상태

- 상태: `verified`
- 제공 자료와 provenance: `study`에서 새로 추가한 입문 과제
