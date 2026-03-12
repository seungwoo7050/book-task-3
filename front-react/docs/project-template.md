# 프로젝트 템플릿과 프로비넌스 규칙

이 저장소의 프로젝트는 트랙마다 구현 디렉터리 이름이 다를 수 있지만, 공개 표면의 계약은 같다. 어떤 프로젝트든 루트에서 내려왔을 때 `문제 -> 답 -> 검증 -> 다음 단계`가 바로 보여야 한다.

## 기본 원칙

- 디렉터리 이름은 lowercase kebab-case를 사용한다.
- 학습 순서는 두 자리 번호 prefix로 고정한다.
- 활성 트랙은 `frontend-foundations`, `react-internals`, `frontend-portfolio`다.
- 문서는 실제 경로와 실제 워크스페이스 명령만 기준으로 쓴다.

## 상태 용어

- `planned`: 문제 경계만 고정되어 있고 구현/검증이 없다.
- `in-progress`: 구현 중이거나 검증이 끝나지 않았다.
- `verified`: 현재 워크스페이스 기준 명시한 검증 명령을 통과했다.
- `archived`: 더 이상 핵심 활성 경로가 아니다.

## 프로비넌스 용어

- `original`: 원문 자산을 그대로 보존한 자료
- `adapted`: 새 구조에 맞게 경로나 설명을 조정한 자료
- `authored`: 이 저장소를 위해 직접 작성한 자료

## 언어와 주석 정책

- authored README, `docs/`, `notion/`, 설명 주석은 한국어를 기본으로 쓴다.
- 명령어, 파일 경로, 식별자, API 이름, 프로토콜 이름, 패키지 이름은 원문 영어를 유지한다.
- `problem/original/`, 제공 스켈레톤 코드, generated 파일은 번역하거나 문체를 통일하지 않는다.
- 코드 주석은 필요한 경우만 추가하고, 설명 주석은 한국어로 쓴다.

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
    05-development-timeline.md
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
    05-development-timeline.md
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
    05-development-timeline.md
```

## 역할 구분

- `problem/`: 문제 정의, 제공 자산, 제약, canonical verification
- 구현 디렉터리 (`vanilla/`, `ts/`, `next/`): 현재 실행 가능한 답과 테스트
- `docs/`: 공개 개념 문서, 발표 자료, 검증 근거
- `notion/`: 추적 가능한 학습 노트, 개발 타임라인, 디버깅 근거

## 프로젝트 README 계약

각 프로젝트 `README.md`는 반드시 아래 순서를 따른다.

- `무슨 문제인가`
- `왜 필요한가`
- `내가 만든 답`
- `핵심 구현 포인트`
- `검증`
- `읽기 순서`
- `한계`

추가 원칙은 아래를 따른다.

- 문제 설명보다 먼저 구현 세부나 회고를 늘어놓지 않는다.
- `problem/README.md`, 구현 README, `docs/README.md`로 바로 들어가는 링크를 포함한다.
- 검증 섹션에는 명령, 기준일 또는 검증 일시, 통과 범위를 같이 적는다.

## problem README 계약

각 `problem/README.md`는 반드시 아래 항목을 포함한다.

- `문제`
- `제공 자산`
- `제약`
- `포함 범위`
- `제외 범위`
- `요구 산출물`
- `Canonical Verification`

원칙은 아래를 따른다.

- 문제는 "무엇을 구현하라"보다 "무슨 질문에 답해야 하는가"를 먼저 드러낸다.
- `original` 자산이 있으면 provenance를 분리해서 명시한다.
- placeholder 디렉터리가 남아 있다면 그 이유를 적고 실제 구현 자산인 것처럼 설명하지 않는다.

## 검증 표기 원칙

- 명령은 항상 `study/` 워크스페이스 기준으로 쓴다.
- README에 적은 workspace package name은 실제 `package.json`과 일치해야 한다.
- 날짜를 적을 때 exact run timestamp를 모르면 `verified 기준일`이라고 적는다.
- 검증 범위는 테스트 파일 이름 또는 시나리오 이름으로 적어 재현 가능해야 한다.

## `notion/` 운영 규칙

- 이 저장소의 `notion/`은 tracked 학습 노트다. local scratchpad가 아니다.
- 권장 기본 세트는 `00-problem-framing.md`부터 `05-development-timeline.md`까지다.
- `notion/`은 문제 정의, 판단 근거, 실패 기록, 재검증 과정을 압축해서 남긴다.
- public README와 `docs/`만 읽어도 프로젝트를 이해할 수 있어야 한다.
