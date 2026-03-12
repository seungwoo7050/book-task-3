# 재현 가이드

## 실행 환경

- Node.js 18+
- pnpm 패키지 매니저
- TypeScript

## 테스트 실행

```bash
cd problem
make install
make test
```

또는 직접 실행:

```bash
cd solve/solution
pnpm install
pnpm test
```

## 기대 결과

모든 테스트 스위트가 통과해야 한다.

## 검증 흐름

1. `problem/code/` 디렉토리의 문제 정의 확인
2. `docs/` 디렉토리의 설계 문서 참고
3. `solve/solution/` 디렉토리의 구현 코드 확인
4. `make test` 실행하여 전체 테스트 통과 확인

## 주의사항

- 모노레포 구조: 루트 `pnpm-workspace.yaml` 참고
- Express 또는 NestJS 프레임워크 기반
- `tsconfig.base.json` 상속 구조 확인 필요


## 근거 요약

- 근거: [문서] `backend-architecture/05-event-system/README.md`
- 근거: [문서] `backend-architecture/05-event-system/lab-report.md`
- 근거: [문서] `backend-architecture/05-event-system/express-impl/docs/README.md`
- 근거: [문서] `backend-architecture/05-event-system/express-impl/devlog/README.md`
