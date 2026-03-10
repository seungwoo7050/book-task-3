# 03 Mini LSM Store — Notion 문서 가이드

## 이 폴더는 무엇인가

이 `notion/` 폴더는 Mini LSM Store 프로젝트를 블로그형 에세이와 재현 가능한 타임라인으로 정리한 문서 세트다.
01(SkipList)와 02(SSTable)에서 만든 부품을 조립하는 프로젝트이므로, 그 두 프로젝트를 먼저 읽고 오면 이해가 수월하다.

## 문서 목록과 읽는 순서

| 순서 | 문서 | 목적 |
|------|------|------|
| 1 | [essay.md](essay.md) | MemTable과 SSTable을 연결해 LSM Store를 만드는 과정의 에세이. |
| 2 | [timeline.md](timeline.md) | 개발 타임라인. 내부 패키지 복사, CLI, 테스트 순서가 담겨 있다. |

## 목적별 바로가기

- **"LSM Store가 뭔지 빠르게 알고 싶다"** → [essay.md](essay.md) 첫 두 섹션
- **"flush가 어떻게 동작하는지"** → [essay.md](essay.md) "flush" 섹션
- **"read path의 우선순위가 궁금하다"** → [essay.md](essay.md) "읽기 경로" 섹션
- **"코드를 따라 재현하고 싶다"** → [timeline.md](timeline.md)
