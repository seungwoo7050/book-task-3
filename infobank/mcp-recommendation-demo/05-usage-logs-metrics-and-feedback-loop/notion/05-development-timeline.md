# 05 로그, 지표, 피드백 루프 재현 타임라인

## 이 문서의 역할

이 문서는 과거의 상세 일지를 그대로 복사하지 않는다. 대신 지금 저장소 기준으로 같은 학습 결과를 다시 확인하려면 무엇을 어떤 순서로 읽고 실행해야 하는지 정리한다.

## 재현 순서

1. 상위 `README.md`, `problem/README.md`, `docs/README.md`를 읽어 이 stage가 왜 분리됐는지 고정한다.
2. 아래 연결 경로를 위에서 아래 순서로 열어 실제 구현과 문서 설명을 대조한다.

- `08-capstone-submission/v1-ranking-hardening/node/src/db/schema.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/repositories/catalog-repository.ts`
- `08-capstone-submission/v1-ranking-hardening/node/src/app.ts`
- `08-capstone-submission/v1-ranking-hardening/react/components/mcp-dashboard.tsx`

3. `v1-ranking-hardening` 폴더로 이동해 아래 명령으로 실제 동작과 테스트를 확인한다.

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

- 추천 품질 개선이 일회성 실험이 아니라 운영 루프로 설명된다.
- 학생이 자기 프로젝트에서 어떤 운영 지표를 남겨야 할지 감을 잡는다.
- 후속 release gate와 operator console 단계로 자연스럽게 이어진다.

## 학습 체크포인트

- 이 stage를 통해 이해해야 할 핵심 개념: 추천 서비스에서 어떤 로그와 피드백을 남겨야 하는지, 실험 메타데이터를 운영자 콘솔과 연결하는 법, 사용 로그를 다음 실험 설계와 품질 개선으로 잇는 방식
- 이 stage를 포트폴리오로 옮길 때 강조할 것: 피드백 루프와 실험 메타데이터 설계, 운영 로그를 제품 품질 개선 서사로 묶는 방식

## 막히면 먼저 볼 것

- `02-debug-log.md`
- `v1-ranking-hardening`의 README와 docs
- `../notion-archive/05-development-timeline.md`

## 자기 포트폴리오 레포로 옮길 때

- 이 문서의 순서를 그대로 유지하되, 경로만 내 저장소 구조에 맞게 바꾼다.
- `README.md`에는 문제 해석, 현재 상태, 실행 명령만 남기고 더 긴 판단 과정은 `notion/`으로 보낸다.
- `docs/README.md`에는 검증 기준, proof artifact, 오래 남길 개념만 남긴다.
- 새 노트를 다시 쓰고 싶다면 기존 `notion/`을 `notion-archive/`로 옮겨 예전 판단을 보존한다.
- 발표나 제출용 README를 만들 때는 이 문서의 체크포인트를 그대로 acceptance checklist로 재사용한다.
