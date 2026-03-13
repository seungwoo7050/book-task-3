# 00-language-and-typescript structure plan

## 중심 질문

- Express나 NestJS로 가기 전에 어떤 타입 표면을 먼저 고정했는가
- 비동기 inventory 조회 실패를 왜 batch 내부에서 흡수했는가
- CLI 하나가 타입 연습을 실제 runtime 검증으로 바꾸는 지점은 어디였는가

## 10-development-timeline.md

- 오프닝: 이 프로젝트가 "도서 메타데이터를 타입 안정적으로 정규화하는 작은 브리지"라는 점을 먼저 고정한다.
- Phase 1: `normalizeTags()`와 `toNormalizedBook()`으로 입력 draft와 외부 모델을 분리한 장면.
- Phase 2: `fetchInventorySnapshot()`에서 `Promise.all()`과 per-item `try/catch`를 결합해 부분 실패를 흡수한 장면.
- Phase 3: `parseArgs()`와 `runCli()`가 테스트, 에러 메시지, 최종 카드 출력을 하나의 entrypoint로 묶는 장면.
- 강조 포인트: "문법 연습"이 아니라 이후 프로젝트에서도 계속 재사용할 타입 경계와 실패 처리 감각을 먼저 익힌다는 점.
