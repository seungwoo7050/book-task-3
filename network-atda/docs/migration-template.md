
# Migration Template

## 코드 과제 기본 구조

```text
study/<track>/<project>/
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

## 패킷 분석 랩 기본 구조

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
    tests/
  docs/
    README.md
    concepts/
    references/
  notion/
    ...
```

## 상태 어휘

- `planned`
- `in-progress`
- `verified`
- `archived`

## 원칙

- `problem/`은 제공 자료와 검증 래퍼만 둡니다.
- 사용자 구현은 `python/src/` 또는 `analysis/src/`로 분리합니다.
- `docs/`는 짧고 재사용 가능한 개념 메모만 둡니다.
- 과정 로그와 실패 기록은 로컬 전용 `notion/`으로 밀어냅니다.
