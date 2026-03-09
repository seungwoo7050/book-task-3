# 09 Exception & Evidence Manager — Notion 문서 안내

## 이 폴더의 목적

이 `notion/` 폴더는 프로젝트 09-exception-and-evidence-manager의 개발 과정과 학습 내용을
Notion으로 옮길 수 있는 형태로 정리한 문서 세트입니다.

## 문서 목록과 읽기 순서

| 순서 | 문서 | 목적 | 추천 독자 |
|------|------|------|-----------|
| 1 | [essay.md](essay.md) | 보안 예외 관리가 왜 필요한지, 증거 첨부와 감사 로그라는 두 축이 어떻게 맞물리는지를 서사적으로 풀어낸 에세이 | CSPM에서 예외 처리를 설계해야 하는 사람 |
| 2 | [dev-timeline.md](dev-timeline.md) | 데이터 모델 설계부터 승인 흐름, 만료 검사까지 전체 개발 과정의 타임라인 | 프로젝트를 재현하려는 사람 |

## 언제 어떤 문서를 읽을까

- **"보안 예외 관리가 왜 필요한지 이해하고 싶다"** → `essay.md`
- **"suppress/unsuppress 로직을 어떻게 구현하나"** → `essay.md`의 핵심 흐름 섹션
- **"직접 ExceptionManager를 처음부터 만들어 보고 싶다"** → `dev-timeline.md`
- **"감사 추적(audit trail)이 왜 append-only인지 알고 싶다"** → `essay.md`
