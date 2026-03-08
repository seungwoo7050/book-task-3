# Project Template And Provenance Rules

이 저장소의 프로젝트는 트랙마다 구현 디렉터리 이름은 다를 수 있지만, 문제 자산과 구현 자산, 공개 문서, 로컬 노트의 경계는 같은 방식으로 유지한다.

## 디렉터리 규칙

- 이름은 lowercase kebab-case를 사용한다.
- 학습 순서는 두 자리 번호 prefix로 고정한다.
- 활성 트랙은 `frontend-foundations`, `react-internals`, `frontend-portfolio`다.

## 상태 용어

- `planned`
- `in-progress`
- `verified`
- `archived`

## 프로비넌스 용어

- `original`: 레거시에서 그대로 보존한 자료
- `adapted`: 새 구조에 맞게 경로나 설명을 조정한 자료
- `authored`: 새 저장소를 위해 직접 쓴 자료

## 트랙별 표준 구조

### `frontend-foundations`

```text
<project>/
  README.md
  problem/
    README.md
    data/
    script/
  vanilla/
    README.md
    src/
    tests/
  docs/
    README.md
    concepts/
    references/
  notion/
    00-problem-framing.md
    01-approach-log.md
    02-debug-log.md
    03-retrospective.md
    04-knowledge-index.md
```

### `react-internals`

```text
<project>/
  README.md
  problem/
    README.md
    original/
      README.md
    code/
    data/
    script/
  ts/
    README.md
    src/
    tests/
  docs/
    README.md
    concepts/
    references/
  notion/
    00-problem-framing.md
    01-approach-log.md
    02-debug-log.md
    03-retrospective.md
    04-knowledge-index.md
```

### `frontend-portfolio`

```text
<project>/
  README.md
  problem/
    README.md
    data/
    script/
  next/
    README.md
    app/
    src/
    public/
    tests/
  docs/
    README.md
    concepts/
    references/
  notion/
    00-problem-framing.md
    01-approach-log.md
    02-debug-log.md
    03-retrospective.md
    04-knowledge-index.md
```

## 역할 구분

- `problem/`: 문제 정의, 제공 자료, fixtures, 입력 데이터, 실행 스크립트
- 구현 디렉터리 (`vanilla/`, `ts/`, `next/`): 현재 학습자가 실행하는 코드와 테스트
- `docs/`: 저장소에 남길 공개 개념 문서와 발표/검증 자료
- `notion/`: 로컬 전용 과정 로그와 회고

## README 최소 항목

각 프로젝트 README는 반드시 아래를 포함한다.

- 이 프로젝트가 주니어 경로에서 왜 필요한가
- prerequisite
- build/test command
- 현재 상태
- 다음 프로젝트로 이어지는 한계

## tracked 문서 원칙

- README는 문제, 범위, 명령, 상태, 학습 포인트를 빠르게 파악할 수 있어야 한다.
- `docs/`는 durable note와 발표/리뷰 자료만 남긴다.
- `notion/` 없이는 README와 `docs/`를 이해할 수 있어야 한다.

## private note 원칙

- `notion/`은 `.gitignore` 대상이다.
- 로컬 전용이라도 placeholder 한 줄 메모로 두지 않고, 문제 정의와 판단 근거, 불확실성을 완전한 문장으로 남긴다.
- branch, commit, timestamp 등 확인 불가능한 메타데이터를 꾸며 쓰지 않는다.
- 실패 기록과 재시도 내역은 `notion/`으로 보낸다.
