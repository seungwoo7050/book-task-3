# Bytecode IR 노트

## 목적

이 디렉터리는 `bytecode-ir`의 현재 공개용 학습 노트입니다.
공개 README가 탐색용 안내문이라면, 이 폴더는 "어떤 lowering과 VM 구조를 택했는가"와 "새 환경에서 어떤 순서로 다시 검증할 것인가"를 압축한 현재판입니다.

## 이 버전에서 다루는 것

- AST를 어떤 instruction 집합으로 낮췄는가
- closure capture를 어떤 데이터 구조로 명시했는가
- disassembly를 왜 테스트 표면으로 고정했는가
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
- 더 긴 초안이나 실험 로그는 `../notion-archive/`로 옮기고, 현재 `05`는 다시 실행 가능한 압축판으로 유지합니다.
