# 03-rest-api-foundations — Notion 문서 가이드

## 이 폴더의 목적

이 `notion/` 폴더는 프로젝트를 Notion으로 옮길 때 그대로 사용할 수 있는 문서 세트다.
같은 CRUD API를 Express와 NestJS로 나란히 구현한 과정과 비교를 서사적으로 담고 있다.

## 문서 목록과 읽는 순서

| 순서 | 문서 | 설명 |
|------|------|------|
| 1 | [essay.md](essay.md) | 프로젝트 에세이 — Express vs NestJS로 같은 API를 만들며 무엇이 달랐는지 서사적으로 설명한다 |
| 2 | [timeline.md](timeline.md) | 개발 타임라인 — 두 레인의 환경 설정, 구현, 테스트 과정을 순서대로 기록한다 |

## 누가 언제 읽으면 좋은가

- **Express와 NestJS의 차이를 알고 싶은 사람**: `essay.md`를 읽으면 같은 기능을 구현할 때 두 프레임워크가 어떻게 다른지 비교할 수 있다
- **코드를 재현하며 따라가고 싶은 사람**: `timeline.md`를 따라가면 Express 레인과 NestJS 레인 모두 빠짐없이 셋업할 수 있다
- **계층 분리(controller/service)나 DI의 필요성을 체감하고 싶은 사람**: `essay.md`의 해당 섹션을 읽으면 된다
