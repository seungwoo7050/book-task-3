# 10 Cloud Security Control Plane — Notion 문서 안내

## 이 폴더의 목적

이 `notion/` 폴더는 캡스톤 프로젝트 10-cloud-security-control-plane의
전체 개발 과정, 아키텍처 결정, 통합 과정을 Notion으로 옮길 수 있는 형태로 정리했습니다.

## 문서 목록과 읽기 순서

| 순서 | 문서 | 목적 | 추천 독자 |
|------|------|------|-----------|
| 1 | [essay.md](essay.md) | 9개 과제를 하나의 API 서비스로 통합하는 과정에서의 설계 결정과 학습 | 전체 트랙을 끝낸 사람, 포트폴리오로 설명하고 싶은 사람 |
| 2 | [dev-timeline.md](dev-timeline.md) | Docker Compose부터 데모 캡처까지 전체 개발 과정의 타임라인 | 프로젝트를 처음부터 재현하려는 사람 |

## 언제 어떤 문서를 읽을까

- **"캡스톤이 뭘 하는 프로젝트인지 빠르게 알고 싶다"** → `essay.md` 첫 섹션
- **"9개 프로젝트가 어떻게 통합되는지 알고 싶다"** → `essay.md`의 통합 지점 섹션
- **"FastAPI + SQLAlchemy + Worker 패턴이 왜 이렇게 설계되었나"** → `essay.md`
- **"Docker Compose로 PostgreSQL 세팅하는 법"** → `dev-timeline.md`
- **"데모를 처음부터 재현하고 싶다"** → `dev-timeline.md`의 데모 실행 섹션
