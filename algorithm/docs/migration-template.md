# 마이그레이션 템플릿

이 문서는 새 프로젝트를 `study/` 아래에 추가하거나, 기존 프로젝트 문서를 같은 톤으로 다시 쓰고 싶을 때 기준으로 삼는 템플릿이다.

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
        tests/
      cpp/                  # 비교 구현이 있을 때만
        README.md
        src/
        include/
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
      notion-archive/       # 이전 버전 보관본
```

## 문서 역할

- `README.md`: 프로젝트를 처음 보는 사람이 읽는 입구
- `problem/`: 문제 자료, fixture, 실행 스크립트
- `python/`, `cpp/`: 구현과 실행 메모
- `docs/`: 공개용 학습 문서
- `notion/`: 긴 호흡의 공개 학습 노트
- `notion-archive/`: 이전 버전 메모와 백업

## README 권장 섹션

- 트랙 README: `트랙 소개`, `왜 이 순서로 배우는가`, `프로젝트 목록`, `먼저 읽을 문서`, `포트폴리오 팁`
- 프로젝트 README: `문제 한눈에 보기`, `이 프로젝트에서 배우는 것`, `추천 읽기 순서`, `디렉터리 구성`, `검증 방법`, `현재 상태`, `다음 확장 아이디어`
- 구현 README: `구현 범위`, `왜 이 구현을 먼저 보는가`, `실행 명령`, `검증 명령`, `현재 상태`, `구현 메모`
- 공개 문서 README: `이 디렉터리의 역할`, `포함 문서`, `추천 읽기 순서`

## 완료 기준

- 루트 README만 읽어도 이 프로젝트가 무엇을 공부하는지 알 수 있어야 한다.
- `make -C problem test` 같은 재현 명령이 README에 드러나 있어야 한다.
- `05-development-timeline.md`가 있으면 학습자가 구현과 검증 과정을 다시 밟을 수 있어야 한다.
- `notion/`과 `notion-archive/`의 역할이 혼동되지 않아야 한다.
- `legacy/`가 현재 워크스페이스에 없어도 문서가 깨지지 않아야 한다.
