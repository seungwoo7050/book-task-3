# Study Project Template And Status Rules

## Fixed Status Values

- `planned`: 구조는 정했지만 구현/검증이 아직 시작되지 않음
- `in-progress`: 구조와 코드가 있으나 검증이 덜 끝남
- `verified`: 문서에 적은 핵심 빌드/테스트를 실제로 통과함
- `archived`: 유지보수 대상이 아니며 참고용으로만 남김

## Required Public Files Per Lab

각 lab은 최소한 다음 파일을 갖는다.

- `README.md`
- `problem/README.md`
- 구현 디렉터리별 `README.md` (`cpp/README.md` 등)
- `docs/README.md`

## Provenance Rule

- `problem/README.md`에는 “재구성한 문제 설명”임을 명시한다.
- 원본 출처는 `legacy/README.md`, 관련 코드 파일, 관련 문서 경로로 표기한다.
- 원본에 없는 요구사항을 추가했으면 왜 추가했는지 적는다.

## Implementation README Minimum

각 구현 README에는 반드시 다음이 들어간다.

- 다루는 문제 범위
- build command
- test command
- 현재 상태
- known gaps
- 구현 메모

## Public vs Local Notes

- tracked 문서: 문제 요약, 제약, 검증 경로, 설계 이유
- local-only `notion/`: 실패 로그, 회고, 길었던 결정 기록, 개인 혼란 노트

## Notion Rule

- `notion/`은 local-only다.
- Git에는 tracked placeholder를 남기지 않는다.
- public docs는 `notion/`이 없어도 읽히고 실행 가능해야 한다.

## Verification Rule

문서에 적은 명령은 저장소 안 실제 파일 기준으로 실행 가능해야 한다. 실행하지 못한 검증은 `verified`로 표시하지 않는다.

## Repository-Specific Default

- 현재 저장소는 `study/<project>` flat 구조를 기본으로 사용한다.
- 구현 언어는 기본적으로 `cpp/` 하나만 둔다.
- empty scaffolding이 필요하면 `problem/code`, `problem/data`, `problem/script`, `docs/concepts`, `docs/references` 디렉터리를 먼저 만든다.
