# Structure Plan: 01 Bridge Vs JSI

## 글의 중심 질문

- 이 프로젝트는 RN architecture 논쟁을 추상 비교로 남기지 않고, 현재 버전에서 재현 가능한 workload 비교로 바꾸는 것이 핵심이다.

## 구현 순서 요약

- `benchmark.ts`에서 async vs sync surface를 같은 payload로 정의한다.
- `BridgeVsJsiStudyApp.tsx`에서 mean/stddev 결과를 대시보드처럼 노출한다.
- `export-results.mjs`와 테스트로 결과를 JSON artifact까지 확장한다.

## 섹션 설계

1. Phase 1: runtime toggle 대신 workload benchmark로 질문을 재정의한다.
변경 단위: `react-native/src/benchmark.ts`
코드 앵커: `RUNS`
2. Phase 2: benchmark 결과를 RN 화면에서 읽히게 만든다.
변경 단위: `react-native/src/BridgeVsJsiStudyApp.tsx`
코드 앵커: `stats.map(...)`
3. Phase 3: export file과 테스트로 결과를 artifact로 남긴다.
변경 단위: `react-native/scripts/export-results.mjs`, `react-native/tests/bridge-vs-jsi.test.tsx`
코드 앵커: `buildExport()`

## 반드시 넣을 근거

- CLI: `npm run verify`
- verification: current replay 기준 `2`개 테스트 통과, export 파일 재생성
- concept: RN 0.84에서는 runtime toggle보다 JS surface benchmark가 더 실용적이다

## 개념 설명 포인트

- 새로 이해한 것: architecture 질문도 버전과 surface에 맞춰 다시 써야 한다
- 중요한 것은 bridge/JSI 용어 자체보다 같은 workload와 같은 payload size를 유지하는 비교 설계다

## 마무리 질문

- 다음 프로젝트에서는 cost 비교 대신 JS/native boundary를 typed spec과 codegen summary로 설명한다.
