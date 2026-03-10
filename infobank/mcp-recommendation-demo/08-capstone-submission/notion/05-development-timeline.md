# capstone 제출 정리 재현 타임라인

## 이 문서의 역할

이 문서는 버전별 capstone을 같은 순서로 다시 읽고 실행하기 위한 재현 경로를 남긴다. 학생이 자기 포트폴리오 레포를 만들 때도 이 구조를 거의 그대로 가져갈 수 있다.

## 재현 순서

1. 상위 `08-capstone-submission/README.md`와 `problem/README.md`를 읽어 버전별 역할을 고정한다.
2. `v0 -> v1 -> v2 -> v3` 순서로 README와 docs를 읽으며 어떤 범위가 추가되는지 비교한다.
3. 실제 실행은 먼저 `v2-submission-polish`에서 재현하고, 필요하면 `v0`, `v1`, `v3`로 내려가 비교한다.

### v2 제출 마감 재현 명령

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm eval
pnpm compatibility rc-release-check-bot-1-5-0
pnpm release:gate rc-release-check-bot-1-5-0
pnpm artifact:export rc-release-check-bot-1-5-0
pnpm capture:presentation
pnpm test
pnpm e2e
```

### v1 랭킹 강건화 재현 명령

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm dev
pnpm test
pnpm eval
pnpm capture:presentation
pnpm e2e
```

### v0 초기 실행 데모 재현 명령

```bash
pnpm install
cp .env.example .env
pnpm db:up
pnpm migrate
pnpm seed
pnpm dev
pnpm test
pnpm eval
pnpm capture:presentation
pnpm e2e
```

## 체크포인트

- `v2`가 최종 제출 버전으로 읽힌다.
- compare, compatibility, release gate, artifact export가 같은 서사로 연결된다.
- `v3`는 self-hosted 확장 버전으로 별도 역할을 가진다.

## 자기 포트폴리오 레포로 옮길 때

- 이 문서의 순서를 그대로 유지하되, 경로만 내 저장소 구조에 맞게 바꾼다.
- `README.md`에는 문제 해석, 현재 상태, 실행 명령만 남기고 더 긴 판단 과정은 `notion/`으로 보낸다.
- `docs/README.md`에는 검증 기준, proof artifact, 오래 남길 개념만 남긴다.
- 새 노트를 다시 쓰고 싶다면 기존 `notion/`을 `notion-archive/`로 옮겨 예전 판단을 보존한다.
- 발표나 제출용 README를 만들 때는 이 문서의 체크포인트를 그대로 acceptance checklist로 재사용한다.
