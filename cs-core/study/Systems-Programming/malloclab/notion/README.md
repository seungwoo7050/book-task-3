# Malloc Lab 노트

## 목적

이 디렉터리는 `malloclab`의 현재 Notion 업로드본입니다.
`../notion-archive/`가 전체 작업 흔적을 보존한다면, 이 폴더는 다시 복습하고 재현할 때 필요한 판단과 순서를 앞쪽으로 끌어온 현재판입니다.

## 이 버전에서 다루는 것

- allocator를 어떤 불변식으로 나눠 설계했는가
- `realloc`을 마지막까지 미룬 이유는 무엇인가
- 실제로 free list가 무너질 때 무엇부터 봐야 하는가
- 새 환경에서 어떤 순서로 다시 검증하면 되는가
- 이후 다른 시스템 코드와 어떤 습관이 연결되는가

## 권장 읽기 순서

1. `00-problem-framing.md`
2. `05-development-timeline.md`
3. `01-approach-log.md`
4. `02-debug-log.md`
5. `04-knowledge-index.md`
6. `03-retrospective.md`

## 메모

- 공개 README는 탐색용, 이 폴더는 재학습과 재현용이다.
- 더 긴 CLI 이력과 당시 메모는 `../notion-archive/`에 남겨 두고, 현재 `05`는 다시 실행 가능한 압축판으로 유지한다.
