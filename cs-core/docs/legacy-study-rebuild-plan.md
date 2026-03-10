# Legacy Study Rebuild Plan

## 목적

이 문서는 `legacy/`를 읽기 전용 참고 트리로 남겨 두고,
`study/`를 현재 기준의 학습 저장소로 다시 정리할 때 지키는 운영 기준을 모아 둔 문서입니다.

## 현재 기준 정리

- 공개 문서는 한국어 우선으로 정리한다.
- 루트와 트랙 README만 읽어도 저장소 전체 학습 순서를 이해할 수 있어야 한다.
- 프로젝트마다 `problem/`, 구현 디렉터리, `docs/`, `notion/`의 역할을 분리한다.
- 기존 장문 기록은 `notion-archive/`로 보존하고, 현재 `notion/`은 다시 실행 가능한 압축판으로 유지한다.
- 공개 README는 짧고 탐색 가능해야 하며, 긴 로그와 재현 기록은 `notion/` 또는 `notion-archive/`로 보낸다.

## 루트 구조

```text
legacy/
study/
docs/
README.md
```

- `legacy/`: 이전 학습 흔적을 보존하는 읽기 전용 참고 트리
- `study/`: 현재 기준으로 다시 짠 학습 트리
- `docs/`: 저장소 전체 규칙과 마이그레이션 메모

## 트랙 구조

현재 `study/`는 두 트랙으로 나뉩니다.

- `Foundations-CSAPP`: `datalab` -> `bomblab` -> `attacklab` -> `archlab` -> `perflab`
- `Systems-Programming`: `shlab` -> `malloclab` -> `proxylab`

이 순서는 "비트/표현 이해 -> 기계 수준 분석 -> 시스템 구현" 흐름을 분명하게 만들기 위한 현재 기준입니다.

## 프로젝트 템플릿

새 프로젝트를 정리할 때는 아래 구조를 기본으로 씁니다.

```text
study/
  <track>/
    <project>/
      README.md
      problem/
        README.md
        code/
        data/
        script/
      c/
        README.md
        src/
        tests/
      cpp/
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
      notion-archive/
```

## README 템플릿 규칙

공개 README는 가능한 한 같은 순서를 유지합니다.

1. 이 프로젝트 또는 디렉터리가 가르치는 것
2. 누구를 위한 문서인가
3. 먼저 읽을 곳
4. 디렉터리 구조
5. 검증 방법
6. 스포일러 경계
7. 포트폴리오로 확장하는 힌트

이 순서를 쓰는 이유는 학습자가 무엇을 읽고 왜 읽는지 빠르게 판단하게 하기 위해서입니다.

## `notion/` 운영 규칙

- `notion/`은 현재 업로드용 문서다.
- 현재 표준 파일 세트는 `00`~`05`다.
- `05-development-timeline.md`는 재현 순서, 검증 명령, 성공 신호를 압축해서 보존하는 문서다.
- `notion-archive/`는 이전 장문 기록을 보존하는 백업 폴더다.
- 새로 작성할 때는 기존 `notion-archive/`를 삭제하지 않는다.
- 공개 README는 `notion/`을 열지 않아도 프로젝트 구조를 이해할 수 있어야 한다.

## 커리큘럼 설계 규칙

- `legacy/`의 프로젝트 순서를 그대로 따를 의무는 없다.
- 누락된 연결 프로젝트가 있으면 `study/`에 새로 추가할 수 있다.
- 너무 약한 프로젝트는 합치거나 이름을 바꿀 수 있다.
- 프로젝트를 추가하거나 바꿀 때는 어떤 개념 공백을 메우는지 README에 남긴다.

## 검증과 공개 범위

- 명령은 실제 존재하는 파일과 타깃만 가리켜야 한다.
- 검증 경로가 바뀌면 프로젝트 README와 `study/PUBLISHABILITY_REVIEW.md`를 함께 갱신한다.
- 외부 course 자산은 복원 명령만 남기고, 자산 자체는 커밋하지 않는다.

## 포트폴리오로 확장하는 힌트

- 이 운영 기준은 다른 학습 저장소에도 거의 그대로 재사용할 수 있습니다.
- 특히 공개 저장소를 만들 때는 "문제 경계 문서 + 실행 가능한 본인 코드 + 검증 방법 + 회고 + 재현 타임라인" 구조가 가장 안정적입니다.
