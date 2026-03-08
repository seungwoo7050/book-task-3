# Migration Conventions

## Public Directory Shape

각 `study/<track>/<project>/`는 아래 공개 표면을 가진다.

- `README.md`
- `problem/`
- `go/`
- `docs/`

`notion/`은 로컬 전용이며 추적하지 않는다.

## Status Vocabulary

- `planned`: 구조만 생성됐고 구현은 아직 없음
- `in-progress`: 구현 중이며 공개 명령이 일부만 검증됨
- `verified`: 문서에 적힌 빌드/테스트 명령이 실제 통과함
- `archived`: 더 이상 정본 구현 대상으로 확장하지 않음

## Go Layout

Go 구현은 기본적으로 아래 구조를 따른다.

```text
go/
  README.md
  go.mod
  cmd/<project>/
  internal/
  tests/
```

원칙:

- 표준 라이브러리를 우선 사용한다.
- 프로젝트는 독립 모듈로 유지한다.
- 루트 `go.work`는 개발 편의용 연결만 제공하고, 루트 빌드 인터페이스는 제공하지 않는다.
- 문서에 적는 공식 검증 명령은 프로젝트 로컬 `GOWORK=off` 기준으로 적는다.

## Provenance Rules

- `problem/README.md`에는 반드시 `Source Provenance` 섹션을 둔다.
- 원본이 `legacy/`의 어떤 파일에서 왔는지 명시한다.
- 번역, 분할, API 변경이 있으면 무엇이 달라졌는지 적는다.

## Verification Rules

- 공개 README에는 실제로 통과한 명령만 적는다.
- 검증 범위는 최소 `build or compile`, `tests`, `demo or fixture run` 중 해당되는 것을 포함한다.
- 루트 정본 문서는 개별 프로젝트 명령으로만 검증을 안내한다.

## Private Notes

- `study/**/notion/`은 `.gitignore`로 제외한다.
- tracked 파일은 `notion/` 존재를 가정하지 않는다.
- 과정성 로그, 실패 기록, 회고는 `notion/`에서 관리한다.

## Repository-Specific Overrides

- 이 저장소의 정식 구현 언어는 Go 1.26.0이다.
- 초기 웨이브에서는 `grpc`, ORM, 웹 프레임워크를 도입하지 않는다.
- `legacy/`는 읽기 전용 참조로 취급한다.
