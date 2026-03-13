# 02 Types Errors Interfaces Evidence Ledger

## 10 type-model-and-catalog-contracts

- 시간 표지: Phase 1: 프로젝트 뼈대 만들기 -> Phase 2: 도메인 타입 정의 -> Phase 3: Catalog 구현 -> Phase 4: CLI 바이너리 작성 -> Phase 5: 테스트 작성 및 검증 -> Phase 6: 문서 작성 및 최종 검증
- 당시 목표: 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- 변경 단위: `lesson/`, `domain/`, `solution/go/domain/catalog.go`, `solution/go/cmd/inventorydemo/main.go`, `solution/go/domain/catalog_test.go`, `problem/README.md`
- 처음 가설: 가격 계산 규칙을 interface로 분리해 concrete type과 정책 객체의 경계를 드러냈다.
- 실제 조치: 디렉터리 구조 생성 프로젝트 01과 같은 구조를 따르되, 도메인 로직 패키지 이름을 `lesson/` 대신 `domain/`으로 바꿨다. "카탈로그"라는 도메인 개념이 있으니 패키지 이름도 그에 맞춘 것이다. Item struct 작성 (`solution/go/domain/catalog.go`) 가장 먼저 `Item` struct를 정의했다. 세 필드: SKU(문자열), Name(문자열), PriceCents(정수). 가격을 센트 단위로 한 건 부동소수점 오차를 피하기 위해서다.

CLI:

```bash
mkdir -p 00-go-fundamentals/02-types-errors-interfaces/{solution/go/cmd/inventorydemo,solution/go/domain,docs/concepts,docs/references,problem}

cd 00-go-fundamentals/02-types-errors-interfaces/go
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/02-types-errors-interfaces
```

- 검증 신호:
- Catalog을 생성하고 상품 하나를 추가한 뒤 20% 할인된 가격을 출력한다. `log.Fatal`로 에러를 처리한다.
- 출력: starter-pack final price: 2400 cents
- ok   .../02-types-errors-interfaces/domain
- --- PASS: TestCatalogAddDuplicate (0.00s)
- --- PASS: TestCatalogFinalPrice (0.00s)
- 핵심 코드 앵커: `solution/go/domain/catalog.go`
- 새로 배운 것: struct는 상태를, method는 그 상태에 대한 동작을 표현한다.
- 다음: 외부 저장소나 persistence 계층은 포함하지 않았다.
