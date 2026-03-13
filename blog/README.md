# Blog Document System

이 디렉터리는 지원용 문서를 `공통 코어 + 재사용 모듈 + 제출 조립본` 구조로 관리하기 위한 작업 공간입니다.

지금부터는 `blog/modules/`와 `blog/assemblies/`를 기준 source of truth로 사용합니다.  
예전에 만들었던 역할별 초안은 보존용으로만 남겨 두었고, 현재 기준 문서는 아닙니다.

## 한눈에 보기

```text
blog/
├── modules/          # 재사용 가능한 문단/근거 모듈
├── assemblies/       # 실제 제출용 문서 세트
├── assets/captures/  # 제출본에 붙는 canonical capture
├── _legacy/          # 이전 역할별 초안 보관
├── portfolio.md
├── career-description.md
└── self-introduction.md
```

## 무엇이 기준인가

- 기준 문서: `blog/modules/`, `blog/assemblies/`
- 보조 참고: `blog/assets/captures/`
- 이전 초안 보관: `blog/_legacy/roles-previous/`
- 루트의 `portfolio.md`, `career-description.md`, `self-introduction.md`는 초기 공용 초안입니다.

## 폴더 역할

### `modules/`

재사용 가능한 문장 블록과 근거 모듈입니다.  
모든 모듈은 아래 3개 파일을 갖습니다.

- `portfolio.md`
- `career-description.md`
- `self-introduction.md`

대표 모듈은 아래처럼 봅니다.

- `common-core`
  - 42서울, `cs-core`, `network-atda`, `database-systems`
  - 42 상세 사례는 `ft_transcendence`만 사용
- `backend-common`
  - FastAPI 기반 공통 백엔드 기준선
- `frontend`, `go-backend`, `node-backend`, `spring-backend`, `fullstack`, `game-server`
  - 직무별 핵심 가지
- `infobank`, `bithumb`
  - 회사/과제형 제출 보강 모듈

### `assemblies/`

실제로 제출할 때 바로 복사해서 다듬는 문서 세트입니다.  
각 폴더는 하나의 지원 방향을 나타내며, 역시 아래 3개 파일을 갖습니다.

- `portfolio.md`
- `career-description.md`
- `self-introduction.md`

현재 준비된 제출본은 아래 8개입니다.

- `frontend`
- `go-backend`
- `node-backend`
- `spring-backend`
- `fullstack`
- `game-server`
- `infobank`
- `bithumb`

### `assets/captures/`

제출본에 바로 붙일 수 있는 canonical capture 모음입니다.

- 실제 웹 화면 캡처
- 기존 presentation asset
- verification/report 기반 evidence 카드 이미지

현재 환경상 외부 42 프로젝트는 실행 캡처 대신 문서 근거로 처리했습니다.

### `_legacy/`

이전 구조의 역할별 초안 보관용입니다.

- `roles-previous/frontend`
- `roles-previous/fullstack`
- `roles-previous/platform-backend`
- `roles-previous/game-server`

새 작업은 여기서 하지 않습니다.

## 어떤 파일부터 열면 되나

지원 방향별 기본 시작점은 아래처럼 고정합니다.

### 프론트엔드 지원

- [frontend 포트폴리오](/Users/woopinbell/work/book-task-3/blog/assemblies/frontend/portfolio.md)
- [frontend 경력기술서](/Users/woopinbell/work/book-task-3/blog/assemblies/frontend/career-description.md)
- [frontend 자소서](/Users/woopinbell/work/book-task-3/blog/assemblies/frontend/self-introduction.md)

### Go 백엔드 지원

- [go-backend 포트폴리오](/Users/woopinbell/work/book-task-3/blog/assemblies/go-backend/portfolio.md)
- [go-backend 경력기술서](/Users/woopinbell/work/book-task-3/blog/assemblies/go-backend/career-description.md)
- [go-backend 자소서](/Users/woopinbell/work/book-task-3/blog/assemblies/go-backend/self-introduction.md)

### Node 백엔드 지원

- [node-backend 포트폴리오](/Users/woopinbell/work/book-task-3/blog/assemblies/node-backend/portfolio.md)
- [node-backend 경력기술서](/Users/woopinbell/work/book-task-3/blog/assemblies/node-backend/career-description.md)
- [node-backend 자소서](/Users/woopinbell/work/book-task-3/blog/assemblies/node-backend/self-introduction.md)

### Spring 백엔드 지원

- [spring-backend 포트폴리오](/Users/woopinbell/work/book-task-3/blog/assemblies/spring-backend/portfolio.md)
- [spring-backend 경력기술서](/Users/woopinbell/work/book-task-3/blog/assemblies/spring-backend/career-description.md)
- [spring-backend 자소서](/Users/woopinbell/work/book-task-3/blog/assemblies/spring-backend/self-introduction.md)

### 풀스택 지원

- [fullstack 포트폴리오](/Users/woopinbell/work/book-task-3/blog/assemblies/fullstack/portfolio.md)
- [fullstack 경력기술서](/Users/woopinbell/work/book-task-3/blog/assemblies/fullstack/career-description.md)
- [fullstack 자소서](/Users/woopinbell/work/book-task-3/blog/assemblies/fullstack/self-introduction.md)

### 게임서버 지원

- [game-server 포트폴리오](/Users/woopinbell/work/book-task-3/blog/assemblies/game-server/portfolio.md)
- [game-server 경력기술서](/Users/woopinbell/work/book-task-3/blog/assemblies/game-server/career-description.md)
- [game-server 자소서](/Users/woopinbell/work/book-task-3/blog/assemblies/game-server/self-introduction.md)

### 인포뱅크 지원

- [infobank 포트폴리오](/Users/woopinbell/work/book-task-3/blog/assemblies/infobank/portfolio.md)
- [infobank 경력기술서](/Users/woopinbell/work/book-task-3/blog/assemblies/infobank/career-description.md)
- [infobank 자소서](/Users/woopinbell/work/book-task-3/blog/assemblies/infobank/self-introduction.md)

### 빗썸 지원

- [bithumb 포트폴리오](/Users/woopinbell/work/book-task-3/blog/assemblies/bithumb/portfolio.md)
- [bithumb 경력기술서](/Users/woopinbell/work/book-task-3/blog/assemblies/bithumb/career-description.md)
- [bithumb 자소서](/Users/woopinbell/work/book-task-3/blog/assemblies/bithumb/self-introduction.md)

## 실제 사용 순서

### 가장 간단한 사용법

1. 지원 직무에 맞는 `assemblies/<target>/`를 연다.
2. `portfolio.md`, `career-description.md`, `self-introduction.md` 3개를 기본 제출본으로 쓴다.
3. 문서 안의 `삭제 가능 - ...` 블록이 있으면 공고에 맞게 제거한다.
4. 회사명, 지원 동기, 입사 후 기여 문장만 마지막으로 맞춤 수정한다.

### 조금 더 세밀하게 조립하는 법

1. `modules/common-core`를 공통 바닥으로 본다.
2. 직무 가지 모듈 하나를 고른다.
   - 예: `frontend`, `go-backend`, `game-server`
3. 필요하면 보강 모듈을 붙인다.
   - 예: `backend-common`, `infobank`, `bithumb`
4. 그 결과를 `assemblies/` 제출본에 반영한다.

## 조립 규칙

현재 문서 설계 기준은 아래와 같습니다.

- `frontend`
  - `common-core` + `frontend`
- `go-backend`
  - `common-core` + `backend-common` + `go-backend`
  - 필요 시 `infobank` 또는 `bithumb` 보강
- `node-backend`
  - `common-core` + `backend-common` + `node-backend`
  - 필요 시 `infobank` 또는 `bithumb` 보강
- `spring-backend`
  - `common-core` + `backend-common` + `spring-backend`
  - 필요 시 `infobank` 또는 `bithumb` 보강
- `fullstack`
  - `common-core` + `backend-common` + `frontend` + `fullstack`
- `game-server`
  - `common-core` + `game-server`
- `infobank`
  - `common-core` + `backend-common` + `infobank`
- `bithumb`
  - `common-core` + `backend-common` + `bithumb`

## 작성 규칙

### 42서울

- 42 상세 사례는 `ft_transcendence`만 사용
- 표현 고정:
  - Django 백엔드 전담
  - 42 OAuth 기반 원격 인증
  - JWT
  - TOTP 기반 2FA
  - OpenAPI 문서화
- `minishell`, `irc`, `raytracing`는 팀과제 보조 사례로만 짧게 사용

### `mini-vrew`

- `frontend`와 `fullstack`의 대표 프로젝트로 사용
- `go/node/spring/game-server` 기본 제출본에서는 전면에 두지 않음

### 캡처

- 웹 프로젝트는 실제 화면 캡처 우선
- 이미지가 없으면 verification/report 기반 evidence 카드 사용
- 외부 42 프로젝트는 실행 캡처 없이 문서 근거만 사용

## 수정할 때 주의

- 새로 문서를 고칠 때는 `_legacy`가 아니라 `modules` 또는 `assemblies`를 수정합니다.
- 특정 지원처에 맞춘 일회성 수정은 `assemblies`에서 하는 것이 안전합니다.
- 구조 자체를 바꿀 때만 `modules`를 수정합니다.
- `algorithm`은 본문 핵심에 넣지 않습니다.

## 추천 작업 방식

- 빠른 제출:
  - `assemblies/<target>` 3개 문서만 열어서 다듬기
- 여러 공고에 반복 지원:
  - `modules`를 기준으로 문장 재사용
- 회사 맞춤 보강:
  - `infobank`, `bithumb` 모듈을 선택적으로 부착

## 현재 한계

- 외부 42 프로젝트는 현재 실행 환경상 직접 캡처를 다시 만들지 못했습니다.
- 그래서 `ft_transcendence`는 README, OpenAPI, 인증/2FA 코드 흔적을 근거로 정리했습니다.
- 일부 backend/game/server 근거 이미지는 실제 GUI 캡처가 아니라 evidence 카드 형식으로 대체했습니다.

이 README를 기준으로 앞으로는 `assemblies`를 제출본, `modules`를 재사용 소스라고 생각하면 됩니다.
