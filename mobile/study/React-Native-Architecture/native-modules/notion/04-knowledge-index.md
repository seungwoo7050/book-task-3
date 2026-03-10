# 04 — Knowledge Index: 네이티브 모듈 빠른 참조

## 소스 파일 맵

| 파일 | 역할 |
|------|------|
| `react-native/App.tsx` | 진입점. NativeModulesStudyApp 렌더링 |
| `src/specs.ts` | `MODULE_SPECS` 상수 (as const), `buildGeneratedSummary()` 함수 |
| `src/NativeModulesStudyApp.tsx` | Consumer UI. MODULE_SPECS를 카드로 표시 |
| `scripts/codegen-summary.mjs` | generated/modules.json 생성 Node.js 스크립트 |
| `tests/native-modules.test.tsx` | 2개 테스트 (spec 구조, codegen summary) |

## Module Spec 정의

### BatteryModule (3 methods)

| 메서드 | 패턴 |
|--------|------|
| `getBatteryLevel` | 단발 조회 |
| `getChargingStatus` | 단발 조회 |
| `subscribe` | 이벤트 구독 |

### HapticsModule (3 methods)

| 메서드 | 패턴 |
|--------|------|
| `vibrate` | fire-and-forget |
| `impactFeedback` | fire-and-forget |
| `notificationFeedback` | fire-and-forget |

### SensorModule (4 methods)

| 메서드 | 패턴 |
|--------|------|
| `startAccelerometer` | 리소스 시작 |
| `stopAccelerometer` | 리소스 정리 |
| `startGyroscope` | 리소스 시작 |
| `stopGyroscope` | 리소스 정리 |

## Codegen Summary

```json
[
  { "module": "BatteryModule", "methodCount": 3 },
  { "module": "HapticsModule", "methodCount": 3 },
  { "module": "SensorModule", "methodCount": 4 }
]
```

## 의존성 목록

| 패키지 | 버전 | 용도 |
|--------|------|------|
| `react` | 19.2.3 | UI 프레임워크 |
| `react-native` | 0.84.1 | 모바일 프레임워크 |
| `@testing-library/react-native` | ^13.3.3 | 컴포넌트 테스트 |
| `typescript` | ^5.8.3 | 타입 체크 |
| `jest` | ^29.6.3 | 테스트 러너 |

> 서드파티 의존성 없음. RN 코어와 테스트 유틸리티만 사용.

## Makefile 타겟

| 타겟 | 동작 |
|------|------|
| `make test` / `make verify` | `script/verify_task.sh` |
| `make codegen` | `npm run codegen` → generated/modules.json |
| `make app-build` | `npm run typecheck` |
| `make app-test` | `npm test` |
| `make clean` | node_modules, ios/build, android/build, generated 삭제 |

## npm 스크립트

| 스크립트 | 동작 |
|---------|------|
| `npm test` | Jest 실행 |
| `npm run typecheck` | tsc --noEmit |
| `npm run codegen` | codegen-summary.mjs → generated/modules.json |
| `npm run verify` | codegen → typecheck → test (순서 중요) |

## 핵심 개념 문서

| 파일 | 내용 |
|------|------|
| `docs/concepts/spec-and-codegen.md` | spec → codegen → consumer 파이프라인 설명 |

## 연관 프로젝트

| 프로젝트 | 관계 |
|----------|------|
| bridge-vs-jsi | 같은 그룹의 선행 과제. JSI 성능 이점을 벤치마크로 증명 |
| gestures | Haptics 모듈이 gestures의 Vibration.vibrate() 대체안 |
| incident-ops-mobile-client | spec-first 설계 원칙이 캔스톤의 contract-first 패턴과 대응 |
