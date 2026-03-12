# 문제 정의

프로비넌스: `adapted`

## 문제

직접 만든 runtime이 실제 상호작용 앱 위에서 어디까지 버틸 수 있는지 보여 주기 위해, shared runtime을 그대로 import해 검색, 페이지네이션, metrics를 갖춘 consumer app을 만든다.

## 제공 자산

- [original/README.md](original/README.md): 레거시 source map
- `code/`: 공통 디렉터리 shape를 유지하기 위한 placeholder
- `script/`: 공통 디렉터리 shape를 유지하기 위한 placeholder
- `data/`: 별도 입력 데이터가 없어 placeholder만 유지

## 제약

- runtime 코드를 복사하지 않고 `@front-react/hooks-and-events`를 직접 소비해야 한다.
- debounced search와 pagination이 같은 UI에서 함께 동작해야 한다.
- metrics는 학습용 관찰값으로만 다루고 production profiler처럼 주장하지 않는다.

## 포함 범위

- shared runtime consumer app
- debounced search
- load-more pagination
- render metrics panel
- integration-style 검증

## 제외 범위

- 실제 infinite scroll observer
- network layer와 persistence
- production-grade performance profiling

## 요구 산출물

- `ts/`에 실행 가능한 runtime consumer app 구현
- shared runtime consumption과 limitation을 설명하는 공개 문서
- debounce, pagination, metrics를 검증하는 테스트

## Canonical Verification

```bash
cd study
npm run verify --workspace @front-react/runtime-demo-app
```

- `demo.test.ts`: debounce, load more, metrics panel 유지 확인
