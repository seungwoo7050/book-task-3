# 저장소 문서 안내

이 디렉터리는 `study/` 아래의 개별 lab을 읽기 전에 먼저 확인하면 좋은 상위 문서 모음이다. 여기서 해야 하는 일은 세 가지다. 이 레포가 무엇을 배우게 하려는지 이해하고, 프로젝트 순서가 왜 이렇게 배치됐는지 납득하고, 문서를 어떤 기준으로 읽고 쓸지 맞추는 것이다.

## 먼저 읽을 문서

- [repository-audit.md](repository-audit.md): 현재 저장소가 어떤 상태인지, 어떤 전제를 버리고 무엇을 남겼는지 정리한다.
- [curriculum-map.md](curriculum-map.md): 6개 lab이 서로 어떻게 이어지는지, 왜 IRC capstone과 game-server capstone을 둘 다 두는지 설명한다.

## 이 문서들이 도와주는 것

- 새 학습자가 지금 어느 프로젝트를 읽어야 할지 결정하게 돕는다.
- 문서 내용이 실제 파일과 검증 명령을 기준으로 쓰이게 만든다.
- 나중에 자기 포트폴리오 레포를 만들 때 어떤 정보 구조를 가져가면 좋은지 보여 준다.

## 현재 저장소 운영 기준

### 상태 값

- `planned`: 구조와 목표만 정했고 구현/검증은 아직 시작하지 않음
- `in-progress`: 구현은 시작했지만 문서에 적은 핵심 검증이 끝나지 않음
- `verified`: 문서에 적은 핵심 빌드/테스트를 실제로 다시 실행해 통과함
- `archived`: 유지보수 대상이 아니라 참고용으로만 남김

### 공개 문서 최소 구조

각 lab은 다음 문서를 기본으로 둔다.

- `README.md`
- `problem/README.md`
- `cpp/README.md`
- `docs/README.md`
- `notion/README.md`
- `notion/00-problem-framing.md`
- `notion/01-approach-log.md`
- `notion/02-debug-log.md`
- `notion/03-retrospective.md`
- `notion/04-knowledge-index.md`

### `notion/`과 `notion-archive/`

- `notion/`은 Git에 포함되는 공개용 학습 노트다.
- 새로 다시 쓰고 싶다면 기존 `notion/`을 `notion-archive/`로 이름만 바꿔 보존한다.
- 새 `notion/`은 정리된 현재판, `notion-archive/`는 이전 초안과 세부 타임라인 백업으로 취급한다.

### 검증 원칙

- 문서에 적은 명령은 현재 저장소에서 실제로 실행 가능해야 한다.
- 실행하지 못한 검증은 `verified`로 적지 않는다.
- 존재하지 않는 경로는 직접 링크하지 않는다.

### 문서 원칙

- 공개 문서는 한국어 중심으로 쓰되, 필요한 기술 용어만 영문 병기한다.
- README는 학습 경로와 범위를 설명해야 하고, `notion/`은 왜 그렇게 설계했는지까지 설명해야 한다.
- 정답 복사용 해설집보다, 학생이 자기 포트폴리오 레포를 설계하도록 돕는 문체를 우선한다.
