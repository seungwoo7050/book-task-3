# 지식 인덱스 — 빠른 참조용

## 표준 라이브러리

| 패키지 | 함수 | 용도 |
|--------|------|------|
| `strings` | `FieldsFunc` | 커스텀 구분자로 문자열을 토큰으로 분리 |
| `strings` | `ToLower` | 문자열 소문자 변환 |
| `unicode` | `IsLetter` | 문자 여부 판별 (구분자 정의에 사용) |
| `unicode` | `IsNumber` | 숫자 여부 판별 |
| `sort` | `Strings` | 문자열 슬라이스 정렬 (map 순회 안정성 확보) |
| `fmt` | `Printf` | 포맷 출력 |
| `os` | `Args` | 명령줄 인자 접근 |

## Go 문법 패턴

- **슬라이스 초기화**: `make([]string, 0, len(fields))` — 길이 0, 용량을 미리 잡아 재할당 줄임
- **맵 초기화**: `make(map[string]int, len(words))` — 예상 크기 힌트 제공
- **range 순회**: `for _, word := range words` — 인덱스 무시하고 값만 사용
- **클로저 전달**: `FieldsFunc`에 `func(r rune) bool` 전달

## CLI 명령 정리

```bash
# 모듈 초기화 (최초 1회)
go mod init github.com/woopinbell/go-backend/study/00-go-fundamentals/01-go-syntax-and-tooling

# 실행
cd solution/go
go run ./cmd/toolingdemo
go run ./cmd/toolingdemo "custom input text here"

# 테스트
cd solution/go
go test ./...
go test -v ./...          # 개별 테스트 이름 확인
go test -run TestBuildSummary ./lesson/  # 특정 테스트만 실행
```

## 참고 자료

- [A Tour of Go](https://go.dev/tour/welcome/1) — 입문 문법 기준점
- [Package strings](https://pkg.go.dev/strings) — `FieldsFunc`, `ToLower` 동작 확인
