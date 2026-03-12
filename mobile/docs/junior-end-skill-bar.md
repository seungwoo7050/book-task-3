# Junior-End Skill Bar

이 문서는 이 저장소가 `초보자 -> 주니어 끝자락` 경로를 실제로 증명하려면
어떤 역량 증거가 필요한지 정의한다.
커리큘럼의 모양이 좋은 것과, 그 모양을 실제 구현과 검증으로 채운 것은 다른 일이다.

## What "Junior-End" Means Here

이 저장소에서의 `주니어 끝자락`은 다음을 혼자 재현 가능한 수준으로 뜻한다.

- React Native 앱의 화면 구조와 상태 흐름을 설계하고 구현할 수 있다.
- 리스트 성능, interaction 품질, 오류 복구 같은 모바일 기본기를 다룰 수 있다.
- RN 런타임 경계와 네이티브 연동 비용을 설명하고 작은 구현으로 증명할 수 있다.
- 오프라인 큐, replay, realtime 동기화, 역할 기반 액션을 제품 수준으로 묶을 수 있다.
- 문서, 테스트, 데모, 발표 자료까지 포함해 학습 결과를 타인이 재현할 수 있게 남길 수 있다.

## Evidence Matrix

| Skill Area | What Must Be Proven | Primary Project | Current Status |
| --- | --- | --- | --- |
| Navigation and screen state | Stack, Tab, Drawer, typed params, deep linking | `foundations/navigation` | `verified` |
| Large-list rendering | virtualization, window tuning, measurement, regression checks | `foundations/virtualized-list` | `verified` |
| Interaction quality | gestures, transitions, interruptible animation | `foundations/gestures` | `verified` |
| RN runtime model | Bridge vs JSI cost model and instrumentation | `architecture/bridge-vs-jsi` | `verified` |
| Native boundary | small Swift/Kotlin module with documented JS contract | `architecture/native-modules` | `verified` |
| Offline queue fundamentals | persistent outbox, retry, DLQ, replay baseline | `product-systems/offline-sync-foundations` | `verified` |
| Realtime product flow | local-first chat sync, socket reconnect, duplicate safety | `product-systems/realtime-chat` | `verified` |
| Release realism | build variants, signing/documented distribution path, release checklist | `product-systems/app-distribution` | `verified` |
| System contract thinking | backend contract, seed/demo reproducibility, server boundary | `capstone/incident-ops-mobile` | `verified` |
| Product-level RN execution | auth, list/detail/create, offline recovery, demo-ready UX | `capstone/incident-ops-mobile-client` | `verified` |

## Current Verdict

2026-03-08 기준으로 이 저장소는 `초보자 -> 주니어 끝자락` 경로를 실제 증거로 제공한다.

- 시작점: `navigation`이 화면 구조와 deep linking 기본기를 실제 앱으로 보여 준다.
- 중간 다리: `virtualized-list`, `gestures`, `bridge-vs-jsi`, `native-modules`,
  `offline-sync-foundations`, `realtime-chat`, `app-distribution`이 각 역량 단위를 분리 증명한다.
- 끝점: `incident-ops-mobile`과 `incident-ops-mobile-client`가 시스템/계약과 제품 완성도를 각각 닫는다.

## Minimum Line To Cross

이 기준선은 이제 충족됐다.
남은 과제는 새 빈 슬롯을 더 만드는 일이 아니라, 각 프로젝트의 데모 품질과 산출물을
현재 코드와 맞춰 유지하는 일이다.

## Evidence Rule

각 역량은 다음 네 가지가 동시에 있어야 증거로 인정한다.

1. 공개 가능한 소스코드
2. 재현 가능한 build/test 명령
3. 짧고 명확한 public docs
4. 로컬 `notion/` 기술 노트
