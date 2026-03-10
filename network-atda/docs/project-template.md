# Project Template

현재 저장소에서 새 프로젝트를 추가할 때는 아래 구조를 기준으로 맞추는 것을 권장합니다.

## 구현 프로젝트 기본 구조

```text
study/<track>/<project>/
  README.md
  problem/
    README.md
    Makefile
    code/
    data/
    script/
  python/ or cpp/
    README.md
    src/
    tests/
  docs/
    README.md
    concepts/
    references/
  notion/
    README.md
    00-problem-framing.md
    01-approach-log.md
    02-debug-log.md
    03-retrospective.md
    04-knowledge-index.md
  notion-archive/          # 선택, 이전 노트를 보존할 때만 사용
```

## 패킷 분석 프로젝트 기본 구조

```text
study/Packet-Analysis-Top-Down/<lab>/
  README.md
  problem/
    README.md
    Makefile
    data/
    script/
  analysis/
    README.md
    src/
  docs/
    README.md
    concepts/
    references/
```

## README가 반드시 다뤄야 할 질문

- 이 프로젝트는 무엇을 배우게 하는가?
- 왜 이 트랙의 이 위치에 있는가?
- 어떤 자료가 제공되는가?
- 무엇이 현재 동작하는가?
- 어떤 검증 명령을 실행하면 되는가?
- 어디까지 구현했고 무엇은 아직 하지 않았는가?
- 이것을 포트폴리오 프로젝트로 키우려면 무엇을 추가하면 되는가?

## `notion/` 운영 규칙

- `notion/`은 현재 읽을 공개 백업용 노트입니다.
- 새 형식으로 다시 쓰고 싶다면 기존 `notion/`을 삭제하지 말고 `notion-archive/`로 옮긴 뒤 새 `notion/`을 만듭니다.
- `notion/`은 README보다 더 긴 과정 기록을 담지만, 저장소를 이해하는 데 필수 전제가 되어서는 안 됩니다.

## 상태 어휘

- `planned`
- `in-progress`
- `verified`
- `archived`

## 제출 준비 기준

캡스톤 또는 포트폴리오 제출 전 아래 루브릭으로 self-check 하고 결과를 README에 첨부한다.

→ [guides/submission/submission-readiness-rubric.md](../../guides/submission/submission-readiness-rubric.md)

최소 확인 항목:

```
[ ] 빌드·기동 명령 문서화 및 동작 확인
[ ] 단위·통합 테스트 전체 통과
[ ] baseline 로드 테스트 결과 첨부
[ ] 장애 주입 시나리오 1개 이상 실행 및 보고서
[ ] Evidence Package (변경 전후 메트릭) README 포함
```
