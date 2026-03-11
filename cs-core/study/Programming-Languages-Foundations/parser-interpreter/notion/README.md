# Parser Interpreter 노트

## 목적

이 디렉터리는 `parser-interpreter`의 현재 공개용 학습 노트입니다.
공개 README가 탐색용 안내문이라면, 이 폴더는 "왜 이런 문법과 evaluator 경계를 택했는가"와 "새 환경에서 어떤 순서로 다시 검증할 것인가"를 압축한 현재판입니다.

## 이 버전에서 다루는 것

- 왜 문법을 expression-oriented 코어로 제한했는가
- lexer, parser, evaluator를 어떤 경계로 나눴는가
- closure와 short-circuit에서 어디가 자주 깨지는가
- 2026-03-11 기준 재검증 명령과 성공 신호

## 권장 읽기 순서

1. `00-problem-framing.md`
2. `05-development-timeline.md`
3. `01-approach-log.md`
4. `02-debug-log.md`
5. `04-knowledge-index.md`
6. `03-retrospective.md`

## 메모

- 현재 프로젝트는 `notion/`만으로도 재학습과 재검증이 가능하도록 유지합니다.
- 더 긴 실험 로그나 초안은 `../notion-archive/`로 옮기고, 현재 `05`는 다시 실행 가능한 압축판으로 유지합니다.
