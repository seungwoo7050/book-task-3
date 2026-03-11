# 00 문제 정의와 기준 문서 재현 타임라인

## 이 문서의 역할

이 문서는 과거의 상세 일지를 그대로 복사하지 않는다. 대신 지금 저장소 기준으로 같은 학습 결과를 다시 확인하려면 무엇을 어떤 순서로 읽고 실행해야 하는지 정리한다.

## 재현 순서

1. 상위 `README.md`, `problem/README.md`, `docs/README.md`를 읽어 이 stage가 왜 분리됐는지 고정한다.
2. 아래 연결 경로를 위에서 아래 순서로 열어 실제 구현과 문서 설명을 대조한다.

- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/catalog.ts`
- `projects/01-mcp-recommendation-demo/capstone/v0-initial-demo/shared/src/eval.ts`
- `../../docs/curriculum/reference-spine.md`
- `../../docs/curriculum/project-selection-rationale.md`

3. `v0-initial-demo` 폴더로 이동해 아래 명령으로 실제 동작과 테스트를 확인한다.

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

4. 실행 후에는 아래 항목이 실제로 충족되는지 체크한다.

- tracked 문서만 읽어도 이 트랙이 다루는 문제와 최종 데모 방향을 이해할 수 있다.
- reference spine과 baseline capstone 경로가 문서 안에서 분명히 연결된다.
- 학생이 자기 포트폴리오 레포를 만들 때 어떤 상위 문서가 먼저 필요한지 감이 잡힌다.

## 학습 체크포인트

- 이 stage를 통해 이해해야 할 핵심 개념: reference spine을 먼저 정해 읽어야 할 문서 수를 줄이는 법, capstone 코드를 보기 전에 문제 정의와 평가 기준을 먼저 고정하는 법, 학습용 레포에서 설계 문서와 실제 구현 경로를 연결하는 인덱스 작성법
- 이 stage를 포트폴리오로 옮길 때 강조할 것: 문제 정의 문서와 reference spine을 먼저 세우는 방식, 학습용 레포를 기능 목록이 아니라 커리큘럼으로 설명하는 방식

## 막히면 먼저 볼 것

- `02-debug-log.md`
- `v0-initial-demo`의 README와 docs
- `../notion-archive/05-development-timeline.md`

## 자기 포트폴리오 레포로 옮길 때

- 이 문서의 순서를 그대로 유지하되, 경로만 내 저장소 구조에 맞게 바꾼다.
- `README.md`에는 문제 해석, 현재 상태, 실행 명령만 남기고 더 긴 판단 과정은 `notion/`으로 보낸다.
- `docs/README.md`에는 검증 기준, proof artifact, 오래 남길 개념만 남긴다.
- 새 노트를 다시 쓰고 싶다면 기존 `notion/`을 `notion-archive/`로 옮겨 예전 판단을 보존한다.
- 발표나 제출용 README를 만들 때는 이 문서의 체크포인트를 그대로 acceptance checklist로 재사용한다.
