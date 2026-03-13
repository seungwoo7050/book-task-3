# Structure Plan: 02 Native Modules

## 글의 중심 질문

- 이 프로젝트는 native module 구현 예제가 아니라 boundary 설계 연습이다. spec를 먼저 닫고, consumer surface와 generated summary가 그 spec를 같이 읽는 순서가 중요하다.

## 구현 순서 요약

- `specs.ts`에서 public module contract를 먼저 정의한다.
- `NativeModulesStudyApp.tsx`에서 consumer surface가 같은 vocabulary를 쓰게 한다.
- `codegen-summary.mjs`와 tests로 generated summary를 reproducible artifact로 남긴다.

## 섹션 설계

1. Phase 1: module spec를 먼저 정의한다.
변경 단위: `react-native/src/specs.ts`
코드 앵커: `MODULE_SPECS`
2. Phase 2: consumer 앱이 spec를 직접 렌더링한다.
변경 단위: `react-native/src/NativeModulesStudyApp.tsx`
코드 앵커: `MODULE_SPECS.map(...)`
3. Phase 3: codegen summary를 generated artifact와 테스트로 잠근다.
변경 단위: `react-native/scripts/codegen-summary.mjs`, `react-native/tests/native-modules.test.tsx`
코드 앵커: `buildGeneratedSummary()`

## 반드시 넣을 근거

- CLI: `npm run verify`
- verification: current replay 기준 `2`개 테스트 통과, `generated/modules.json` 재생성
- concept: native boundary의 canonical evidence는 spec/codegen/consumer alignment다

## 개념 설명 포인트

- 새로 이해한 것: native module은 “네이티브 코드 작성”보다 “public contract 설계”로 보는 편이 더 재현 가능하다
- full native build 없이도 boundary clarity를 codegen summary로 증명할 수 있다

## 마무리 질문

- 다음 프로젝트에서는 architecture boundary를 떠나, queue/retry/DLQ 같은 product-system 규칙을 독립 문제로 줄여 본다.
