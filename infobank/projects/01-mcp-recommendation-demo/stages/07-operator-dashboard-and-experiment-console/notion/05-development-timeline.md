# 07 운영자 대시보드와 실험 콘솔 재현 타임라인

## 이 문서의 역할

이 문서는 과거의 상세 일지를 그대로 복사하지 않는다. 대신 지금 저장소 기준으로 같은 학습 결과를 다시 확인하려면 무엇을 어떤 순서로 읽고 실행해야 하는지 정리한다.

## 재현 순서

1. 상위 `README.md`, `problem/README.md`, `docs/README.md`를 읽어 이 stage가 왜 분리됐는지 고정한다.
2. 아래 연결 경로를 위에서 아래 순서로 열어 실제 구현과 문서 설명을 대조한다.

- `projects/01-mcp-recommendation-demo/capstone/v1-ranking-hardening/react/components/mcp-dashboard.tsx`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/react/components/mcp-dashboard.tsx`
- `projects/01-mcp-recommendation-demo/capstone/v2-submission-polish/tests/e2e/recommendation.spec.ts`

3. `v2-submission-polish` 폴더로 이동해 아래 명령으로 실제 동작과 테스트를 확인한다.

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

4. 실행 후에는 아래 항목이 실제로 충족되는지 체크한다.

- 추천 시스템이 단일 API가 아니라 운영 도구까지 포함한다는 점을 보여 준다.
- 학생이 자기 포트폴리오에서 운영자 UI를 어떻게 설명할지 참고할 수 있다.
- 최종 capstone의 화면 중심 시연 경로가 명확해진다.

## 학습 체크포인트

- 이 stage를 통해 이해해야 할 핵심 개념: 운영자 화면에서 무엇을 먼저 보여 줘야 하는지, catalog 관리, 실험 관리, release candidate 관리를 한 콘솔로 묶는 법, 실험 결과와 운영 작업을 같은 정보 구조에서 다루는 방식
- 이 stage를 포트폴리오로 옮길 때 강조할 것: 운영자 대시보드 IA 설계, 실험 콘솔과 release console을 같은 제품 서사로 묶는 방식

## 막히면 먼저 볼 것

- `02-debug-log.md`
- `v2-submission-polish`의 README와 docs
- `../notion-archive/05-development-timeline.md`

## 자기 포트폴리오 레포로 옮길 때

- 이 문서의 순서를 그대로 유지하되, 경로만 내 저장소 구조에 맞게 바꾼다.
- `README.md`에는 문제 해석, 현재 상태, 실행 명령만 남기고 더 긴 판단 과정은 `notion/`으로 보낸다.
- `docs/README.md`에는 검증 기준, proof artifact, 오래 남길 개념만 남긴다.
- 새 노트를 다시 쓰고 싶다면 기존 `notion/`을 `notion-archive/`로 옮겨 예전 판단을 보존한다.
- 발표나 제출용 README를 만들 때는 이 문서의 체크포인트를 그대로 acceptance checklist로 재사용한다.
