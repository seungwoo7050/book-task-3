# Structure Plan: 03 App Distribution

## 글의 중심 질문

- 이 프로젝트는 기능 구현보다 release discipline을 따로 떼어 설명하는 실험이다. 검증된 chat snapshot을 그대로 두고, release channel vocabulary와 env/workflow/rehearsal artifact를 덧붙이는 순서가 중요하다.

## 구현 순서 요약

- `releasePlan.ts`에서 세 채널과 lane/artifact 이름을 먼저 고정한다.
- `releaseConfig.mjs`와 workflow로 env key alignment와 automation wiring을 검증한다.
- `release-rehearsal.mjs`가 local rehearsal summary를 JSON artifact로 남기게 만든다.

## 섹션 설계

1. Phase 1: verified chat snapshot 위에 release channel vocabulary를 얹는다.
변경 단위: `react-native/src/releasePlan.ts`
코드 앵커: `releaseTargets`
2. Phase 2: env example과 workflow를 자동으로 검증한다.
변경 단위: `react-native/scripts/releaseConfig.mjs`, `react-native/scripts/validate-release.mjs`, `.github/workflows/mobile-release.yml`
코드 앵커: `consistentKeys`
3. Phase 3: rehearsal summary를 배포 artifact로 남긴다.
변경 단위: `react-native/scripts/release-rehearsal.mjs`, `react-native/release/rehearsal-summary.json`
코드 앵커: `rehearsal`

## 반드시 넣을 근거

- CLI: `npm run verify`, `npm run release:rehearsal`
- verification: current replay 기준 `2`개 suite, `5`개 테스트 통과, rehearsal summary 재생성
- concept: 공개 저장소의 release discipline은 key alignment와 automation wiring으로 먼저 증명된다

## 개념 설명 포인트

- 새로 이해한 것: 배포 준비 상태는 signed binary보다 summary artifact로 더 명확하게 남는다
- 이 프로젝트의 진짜 출력물은 앱 기능 추가가 아니라 env/workflow/rehearsal 세트다

## 마무리 질문

- 다음 단계에서는 incident domain을 system contract 증명과 product client 완성작으로 의도적으로 분리한다.
