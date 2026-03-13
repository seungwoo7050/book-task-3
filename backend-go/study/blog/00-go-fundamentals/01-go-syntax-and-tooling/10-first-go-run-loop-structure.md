# 01 Go Syntax And Tooling Structure

## 이 글이 답할 질문

- 검증 명령과 공개 surface를 함께 닫고 `verified` 기준을 다시 확인한다.
- CLI보다 문자열 처리 핵심 로직을 먼저 분리해 문법 학습이 I/O 처리에 묻히지 않게 했다.
- 어떤 CLI와 어떤 검증 신호가 이 구간을 닫았는가

## 본문 배치

- 도입: `00-go-fundamentals/01-go-syntax-and-tooling` 안에서 `10-first-go-run-loop.md`가 맡는 구간과 이전 글에서 이어지는 지점을 짧게 고정한다.
- 구현 순서 요약: Phase 1: 프로젝트 뼈대 만들기 -> Phase 2: 핵심 로직 구현 -> Phase 3: CLI 바이너리 작성 -> Phase 4: 테스트 작성 및 검증 -> Phase 5: 문서 작성 -> Phase 6: 최종 검증
- 세션 본문: `solution/go/, problem/, docs/, study/` 순서로 구현 흐름을 복원한다.
- 코드 앵커 1: `solution/go/lesson/lesson.go`
- 코드 앵커 2: `solution/go/cmd/toolingdemo/main.go`
- 코드 설명 초점: 이 조각은 프로젝트의 핵심 판단이 실제 어느 함수와 자료구조에 걸려 있는지 보여 준다. 추상 요약보다 먼저 이 코드를 봐야 구현 순서가 살아난다.
- 개념 설명: `strings.FieldsFunc`는 텍스트를 직접 루프 돌며 자르지 않아도 되는 표준 라이브러리 선택지다.
- 마지막 단락: stdin 입력과 flag 파싱은 현재 범위 밖이라 별도 검증하지 않았다.
