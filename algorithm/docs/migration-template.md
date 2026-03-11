# 마이그레이션 템플릿

이 문서는 기존 프로젝트를 다시 정리하거나 새 프로젝트를 `study/` 아래에 추가할 때, README가 먼저 답해야 할 질문을 고정하기 위한 템플릿이다. 목표는 폴더를 늘리는 것이 아니라 `문제 -> 답 -> 검증 -> 노트` 공개 표면을 흔들리지 않게 만드는 것이다.

## 기본 디렉터리 구조
```text
study/
  <track>/
    <project>/
      README.md
      problem/
        README.md
        Makefile
        code/
        data/
        script/
      python/
        README.md
        src/
      cpp/                  # 비교 구현이 있을 때만
        README.md
        src/
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
      notion-archive/
```

## 프로젝트 README가 반드시 답해야 할 질문
- `문제가 뭐였나`
- `제공된 자료`
- `이 레포의 답`
- `어떻게 검증하나`
- `무엇을 배웠나`
- `현재 한계`

## 하위 README 계약
- `problem/README.md`: 문제 계약과 제공 자료만 보여 주고, 문제 전문 복붙은 피한다.
- `python/README.md`, `cpp/README.md`: canonical 구현 경로와 기준 명령만 먼저 보여 준다.
- `docs/README.md`: 판단 근거를 어디서 읽어야 하는지 안내하고, 엔트리포인트 역할을 대신하지 않는다.
- `notion/README.md`: 공개 노트 인덱스이지만 프로젝트를 처음 이해하는 출발점이 아니다.

## 완료 기준
- 루트 README만 읽어도 이 저장소가 어떤 문제군을 푸는지 알 수 있다.
- 프로젝트 README만 읽어도 공개 답안 위치와 canonical verify command를 즉시 찾을 수 있다.
- `make -C problem test` 또는 동등한 canonical verify command가 표면에 드러나 있다.
- `notion/`과 `notion-archive/`의 역할이 섞이지 않는다.
- 상태 어휘는 `planned`, `in-progress`, `verified`, `archived`만 쓴다.
