# 04-request-pipeline — Notion 문서 가이드

## 이 폴더의 목적

이 `notion/` 폴더는 프로젝트를 Notion으로 옮길 때 그대로 사용할 수 있는 문서 세트다.
요청 파이프라인(validation, error handling, logging, response shaping)을 직접 구축한 과정을 담고 있다.

## 문서 목록과 읽는 순서

| 순서 | 문서 | 설명 |
|------|------|------|
| 1 | [essay.md](essay.md) | 프로젝트 에세이 — 요청 파이프라인을 왜 만들고 무엇을 배웠는지 서사적으로 설명한다 |
| 2 | [timeline.md](timeline.md) | 개발 타임라인 — Zod, class-validator, 인터셉터 등을 도입하며 거친 전체 과정을 순서대로 기록한다 |

## 누가 언제 읽으면 좋은가

- **validation이나 에러 처리를 어떻게 공통화하는지 궁금한 사람**: `essay.md`를 읽으면 된다
- **Express 미들웨어와 NestJS 인터셉터/필터의 차이를 이해하고 싶은 사람**: `essay.md`의 비교 섹션을 읽으면 된다
- **코드를 처음부터 재현하고 싶은 사람**: `timeline.md`를 따라가면 된다
