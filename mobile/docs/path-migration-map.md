# Path Migration Map

이번 개편에서는 과거 track 중심 경로를 역량 단계 중심 경로로 옮겼다.
기존 경로와 새 경로의 대응은 아래 표를 따른다.

| 이전 경로 | 새 경로 |
| --- | --- |
| `study/Mobile-Foundations/navigation` | `study/foundations/01-navigation-patterns` |
| `study/Mobile-Foundations/virtualized-list` | `study/foundations/02-virtualized-list-performance` |
| `study/Mobile-Foundations/gestures` | `study/foundations/03-gestures-and-reanimated` |
| `study/React-Native-Architecture/bridge-vs-jsi` | `study/architecture/01-bridge-vs-jsi` |
| `study/React-Native-Architecture/native-modules` | `study/architecture/02-native-modules` |
| `study/Chat-Product-Systems/offline-sync-foundations` | `study/product-systems/01-offline-sync-foundations` |
| `study/Chat-Product-Systems/realtime-chat` | `study/product-systems/02-realtime-chat` |
| `study/Chat-Product-Systems/app-distribution` | `study/product-systems/03-app-distribution` |
| `study/Incident-Ops-Capstone/incident-ops-mobile` | `study/capstone/01-incident-ops-mobile` |
| `study/Incident-Ops-Capstone/incident-ops-mobile-client` | `study/capstone/02-incident-ops-mobile-client` |

## 이행 원칙

- 내부 문서와 검증 명령은 모두 새 경로를 기준으로 갱신한다.
- 옛 경로 호환용 shim 디렉터리는 두지 않는다.
- `SOURCE-PROVENANCE.md`는 과거 경로를 히스토리 정보로만 남길 수 있다.
