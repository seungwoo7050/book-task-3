# Migration Conventions

이 문서는 현재 `database-systems` 레포에서 프로젝트를 이동하거나 새로 추가할 때 지켜야 하는 표면 계약을 정리합니다.

## 현재 프로젝트 배치

- Go 프로젝트: `go/<track>/projects/<nn-slug>/`
- Python 프로젝트: `python/<track>/projects/<nn-slug>/`
- Go 공용 utility: `go/shared/`

## 각 프로젝트가 드러내야 하는 것

- 무엇을 구현해야 하는가: `problem/README.md`
- 이 레포가 실제로 채택한 해법은 무엇인가: 프로젝트 `README.md`
- 어떤 개념 메모와 참고자료가 있는가: `docs/README.md`
- 어떤 시행착오와 회고가 남아 있는가: `notion/README.md`
- 무엇이 과거 버전 문서인가: `notion-archive/README.md`

## 이동 시 체크리스트

- 프로젝트 루트가 바뀌면 README의 `cd` 경로와 검증 명령을 먼저 갱신합니다.
- Go 코드는 module root `go/go.mod` 기준 import path를 사용합니다.
- 상대 링크는 deep link redirect를 두지 않고 전면 갱신합니다.
- provenance 설명은 유지하되, 현재 레포에 없는 옛 경로를 현재 구조처럼 약속하지 않습니다.
