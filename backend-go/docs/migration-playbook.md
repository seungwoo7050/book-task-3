# Migration Playbook

## 원칙

1. 상위 커리큘럼 구조는 `study/<track>/<project>`로 유지한다.
2. 프로젝트 내부는 `problem/`, `solution/`, `docs/`, `notion/`으로 분리한다.
3. 구현 경로는 `solution/go` 또는 `solution/infra`로 통일한다.
4. README는 GitHub 첫 방문자가 `문제`, `답`, `검증`을 바로 이해할 수 있게 작성한다.
5. `verified` 상태는 실제 명령 실행을 근거로만 부여한다.

## 공개 문서와 보조 문서

- `README.md`: 문제 요약, 내 답, 검증, 읽는 순서
- `problem/README.md`: canonical 문제 정의와 성공 기준
- `solution/README.md`: 구현 범위와 진입 명령
- `docs/`: 개념 설명, 참조 문서, 검증 메모
- `notion/`: 접근 로그, 디버그 기록, 회고, 개발 타임라인
