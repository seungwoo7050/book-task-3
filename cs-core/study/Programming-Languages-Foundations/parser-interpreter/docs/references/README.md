# 참고 자료

## 1. Crafting Interpreters

- 출처 유형: 책
- 확인일: 2026-03-11
- 왜 참고했는가: token, parser, tree-walk interpreter를 작은 언어 하나로 엮는 기본 설계를 잡기 위해 참고했습니다.
- 무엇을 반영했는가: recursive descent parser와 environment 기반 evaluator라는 전체 구조를 현재 프로젝트에 맞게 압축했습니다.

## 2. Types and Programming Languages

- 출처 유형: 책
- 확인일: 2026-03-11
- 왜 참고했는가: 같은 언어를 뒤 단계의 static typing 실험으로 이어 붙이기 위한 type surface를 정리하기 위해 참고했습니다.
- 무엇을 반영했는가: `Int`, `Bool`, function type 표면과 static/runtime error 경계 설명에 반영했습니다.

## 3. Essentials of Compilation

- 출처 유형: 책
- 확인일: 2026-03-11
- 왜 참고했는가: 이후 `bytecode-ir` 단계에서 AST 이후 표현을 어떻게 분리할지 미리 염두에 두기 위해 참고했습니다.
- 무엇을 반영했는가: 현재 단계에서는 type annotation을 AST에 보존하고, 뒤 단계에서 같은 문법을 다시 낮출 수 있도록 표면을 고정했습니다.

## 4. CURRICULUM_EXPANSION_PLAN.md

- 출처 유형: 워크스페이스 계획 문서
- 확인일: 2026-03-11
- 왜 참고했는가: `cs-core` PL/컴파일러 확장의 source of truth로 사용하기 위해 참고했습니다.
- 무엇을 반영했는가: 트랙 순서, guide 연계, self-contained project 원칙을 현재 프로젝트 문서에 반영했습니다.
