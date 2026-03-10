# AGENTS.md

## 목적

이 서브트리는 FastAPI 백엔드 학습용 저장소다. 목표는 기능만 나열된 답안집이 아니라, 학생이 코드를 실행하고 문서를 읽으면서 자기만의 포트폴리오용 백엔드 레포를 설계할 수 있게 돕는 것이다.

## 현재 구조

- `labs/`: 주제별 독립 FastAPI 랩
- `capstone/`: 앞선 랩의 개념을 재구성한 통합 백엔드
- `docs/`: 저장소 공통 기준, 커리큘럼, 검증 기록, 템플릿
- `tools/`: 로컬 검증 보조 스크립트

이 서브트리에는 `legacy/`나 `study2/` 같은 별도 트랙이 없다. 존재하지 않는 트랙을 전제로 문서를 쓰지 않는다.

## 작업 원칙

- 문서는 한글 우선으로 작성한다. 필요한 기술 용어만 영어를 병기한다.
- 초중급 학습자가 읽는다고 가정하고, 범위와 단순화 지점을 숨기지 않는다.
- 애플리케이션 동작을 바꾸지 않아도 되는 요청이라면, 문서와 저장소 메타데이터 정리에 집중한다.
- 코드나 문서를 수정할 때는 현재 레포에 실제로 존재하는 파일, 명령, 워크플로우만 근거로 삼는다.
- 검증 보고서에는 마지막 실제 실행 시점을 명시한다. 다시 실행하지 않은 내용을 새 검증처럼 쓰지 않는다.

## 랩 구조 규칙

각 랩과 capstone은 아래 공개 디렉터리를 기준으로 설명한다.

```text
README.md
problem/
fastapi/
docs/
notion/
notion-archive/   # 과거 노트를 보관할 때만 존재
```

`fastapi/` 문서는 최소한 아래 항목을 근거로 작성한다.

```text
app/
tests/
alembic/
pyproject.toml
.env.example
Dockerfile
compose.yaml
Makefile
README.md
```

## notion 정책

- `notion/`은 현재 공개용 학습 노트다.
- 기존 노트를 다시 쓰려면 삭제하지 말고 `notion-archive/`로 옮긴 뒤 새 `notion/`을 만든다.
- 새 `notion/`은 아래 파일 세트를 유지한다.

```text
00-problem-framing.md
01-approach-log.md
02-debug-log.md
03-retrospective.md
04-knowledge-index.md
05-development-timeline.md
README.md
```

## 문서 품질 기준

- 루트 README와 각 랩 README만 읽어도 학습 목표, 실행 경로, 검증 방법을 이해할 수 있어야 한다.
- `problem/`은 문제 정의와 성공 기준을 설명한다.
- `docs/`는 설계 포인트와 개념 지도를 제공한다.
- `notion/`은 학습 로그와 재사용 가능한 지식을 정리한다.
- 절대 로컬 경로 링크는 남기지 않는다. Markdown 링크는 상대 경로로 통일한다.

## 저장소 정리 규칙

- `.env`, 로컬 DB, 캐시, `*.egg-info/`는 추적하지 않는다.
- workflow는 현재 존재하는 경로만 가리켜야 한다.
- 복붙으로 남은 잘못된 프로젝트 이름이나 오래된 설명은 즉시 정리한다.

## 완료 기준

한 번의 문서 정리 작업이 끝났다고 말하려면 아래 조건이 충족되어야 한다.

- 존재하지 않는 경로, 트랙, 절대 링크가 문서에서 제거되었다.
- `notion/`과 `notion-archive/`의 역할이 명확하다.
- 각 랩 README가 학습 목표, 실행, 검증, 확장 아이디어를 안내한다.
- 검증 보고서가 마지막 실제 실행 날짜를 숨기지 않는다.
