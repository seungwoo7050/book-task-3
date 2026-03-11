# Project Template

현재 저장소에서 새 프로젝트를 추가할 때는 아래 구조와 README 계약을 기준으로 맞추는 것을 권장합니다.

## 구현 프로젝트 기본 구조

```text
study/<stage>/<project>/
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
    05-development-timeline.md
  notion-archive/          # 선택, 이전 노트를 보존할 때만 사용
```

## 패킷 분석 프로젝트 기본 구조

```text
study/03-Packet-Analysis-Top-Down/<lab>/
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

## 프로젝트 README가 반드시 다뤄야 할 질문

- `문제가 뭐였나`
- `제공된 자료`
- `이 레포의 답`
- `어떻게 검증하나`
- `무엇을 배웠나`
- `현재 한계`

## 하위 README 계약

- `python/README.md`, `cpp/README.md`, `analysis/README.md`, `docs/README.md`는 모두 `이 폴더의 역할`, `먼저 볼 파일`, `기준 명령`, `현재 범위`, `남은 약점`을 보여 줍니다.
- `notion/README.md`는 공개 노트의 인덱스지만 엔트리포인트가 아닙니다.

## `notion/` 운영 규칙

- `notion/`은 현재 읽을 공개 백업용 노트입니다.
- 새 형식으로 다시 쓰고 싶다면 기존 `notion/`을 삭제하지 말고 `notion-archive/`로 옮긴 뒤 새 `notion/`을 만듭니다.
- `notion/`은 README보다 긴 과정 기록을 담지만, 저장소를 이해하는 데 필수 전제가 되어서는 안 됩니다.

## 상태 어휘

- `planned`
- `in-progress`
- `verified`
- `archived`
