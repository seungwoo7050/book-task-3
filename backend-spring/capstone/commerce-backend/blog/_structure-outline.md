# commerce-backend structure outline

## 글 목표

- 7개 랩의 학습을 baseline commerce로 다시 묶는 과정을 복원한다.
- macOS + VSCode 통합 터미널 기준의 검증 흐름을 유지한다.

## 글 순서

1. auth, catalog, cart, order surface를 먼저 고정한 단계
2. modular monolith baseline을 세운 단계
3. 왜 이 버전이 기준선인지 닫는 단계

## 반드시 넣을 코드 앵커

- `CommerceApiTest.catalogCartAndOrderFlowWork()`
- `CommerceService.checkout()`
- `CommerceAuthController.login()`

## 반드시 넣을 CLI

```bash
cd spring
make test
make smoke
docker compose up --build
```

## 핵심 개념

- baseline capstone은 완성도보다 비교 가능성이 중요하다.
- 일부러 남긴 빈칸이 있어야 v2의 개선 축이 선명해진다.
