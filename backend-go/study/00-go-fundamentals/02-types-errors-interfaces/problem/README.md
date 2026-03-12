# 문제 정의

작은 상품 카탈로그를 만들고, struct와 interface를 사용해 가격 계산 규칙을 분리한다.

## 성공 기준

- SKU 중복 추가를 막는다.
- 존재하지 않는 상품 조회 시 custom error를 반환한다.
- 할인 규칙을 interface로 분리한다.

## 제공 자료와 출처

- `study`에서 새로 설계한 입문형 canonical 문제다.
- 이 문서가 공개용 문제 정의다.
- 공개 구현은 [`solution/README.md`](../solution/README.md)와 `solution/go`에 둔다.

## 검증 기준

- `cd solution/go && go run ./cmd/inventorydemo`
- `cd solution/go && go test ./...`

## 제외 범위

- DB 연동
- mock 프레임워크 활용
