> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Source Brief — 왜 "문서를 코드로 고정하는 일"부터 시작했는가

## 출발점

프로젝트를 시작할 때 가장 먼저 드는 생각은 "빨리 뭘 만들자"였다.
상담 챗봇 품질 관리라는 주제가 정해져 있었고, 최종 결과물은 QA Ops 플랫폼 데모였으니, 바로 평가 파이프라인부터 짜고 싶은 충동이 있었다.

그런데 한 가지 문제가 있었다.
이 프로젝트는 legacy 저장소(`docs/legacy-intent-audit.md`)와 커리큘럼 문서(`docs/curriculum-map.md`, `docs/reference-spine.md`)가 이미 존재하고, 그 문서들이 말하는 방향이 미묘하게 다를 수 있었다.
누군가는 "챗봇을 만든다"고 읽을 수도 있고, 다른 사람은 "챗봇의 품질을 관리하는 도구를 만든다"고 읽을 수도 있었다.

## 이 단계가 해결하려는 것

Source Brief의 핵심 질문은 이것이다:

> "이 트랙이 무엇을 만들고, 어떤 기술 스택과 순서를 따르는지를 코드 한 곳에서 고정할 수 있는가?"

이걸 README 한 줄로 쓰면 끝나지 않느냐고 물을 수 있다. 하지만 경험적으로, 서술형 README는 시간이 지나면 실제 구현과 어긋난다.
"Python 3.12로 간다"고 써놓고 3.14에서 돌리다가 `chromadb`가 깨지는 일이 실제로 생겼다.
그래서 "서술이 아니라 코드 객체로 고정하자"는 결론이 나왔다.

## 성공 기준

이 단계를 마치면 아래 세 가지가 확보된다:

1. **주제, capstone 목표, baseline 버전, 기술 스택**이 `SourceBrief`라는 하나의 frozen dataclass에 정리된다.
2. **Reference spine**(핵심 참조 문서 목록)이 임의 서술이 아니라 테스트 가능한 상수 tuple로 유지된다.
3. 후속 stage(01~08)가 이 brief를 설계 기준으로 **재사용**할 수 있다.

## 이것이 아닌 것

이 단계는 실제 evaluator나 dashboard가 "동작한다"는 걸 입증하지 않는다.
오직 **설계 방향을 코드 계약으로 고정하는 것**이 전부다.
실행 가능한 기능은 stage 02부터 나타나기 시작한다.

## 이 트랙을 처음 보는 사람을 위한 전제

- 이 프로젝트의 목표는 "상담 챗봇을 만드는 것"이 **아니다**. 상담 챗봇의 **품질을 정의하고, 자동 평가하고, 모니터링하는 QA Ops 플랫폼**을 만드는 것이다.
- capstone 최종 결과물은 `08-capstone-submission/v0-initial-demo`를 baseline으로 삼아 `v1`, `v2`, `v3`로 확장된다.
- 주력 스택은 Python 3.12 + FastAPI + Pydantic + SQLAlchemy + React + PostgreSQL + Langfuse다.
