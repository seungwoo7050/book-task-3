# Study Workspace

이 디렉터리는 현재 저장소의 활성 학습 경로를 담는다. 이 저장소에서는 `notion/`도 공개 가능한 현재판 학습 노트로 Git에 포함한다.

## 활성 트랙

- [Node-Backend-Architecture](Node-Backend-Architecture/README.md)

## 현재 그룹 구조

- `bridge/`: 언어, 런타임, HTTP 기본기를 먼저 고정하는 입문 브리지
- `core/`: Express와 NestJS를 비교하며 API, auth, persistence, event를 배우는 코어 단계
- `applied/`: 운영성, capstone, recruiter-facing 서비스까지 연결하는 적용 단계

## 사용 원칙

- 프로젝트 상태는 `verified`, `reverify-blocked`, `in-progress`, `reference-only`로 표시한다.
- 각 프로젝트는 `README -> problem -> 구현 레인 -> docs -> notion` 공개 계약을 따른다.
- 장문 설명은 `docs/`와 `notion/`로 보내고, 프로젝트 README는 빠른 인덱스 역할에 집중한다.
