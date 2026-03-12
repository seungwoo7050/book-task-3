# mobile

이 저장소는 React Native 학습 결과물을 모아 둔 아카이브다. 핵심은 앱 개수를 늘리는 것이 아니라,
각 프로젝트가 "무슨 문제를 풀었는가", "어떤 답을 만들었는가", "어떻게 다시 검증하는가"를
GitHub 표면에서 바로 읽히게 하는 데 있다.

공개 동선은 다음 순서를 기준으로 읽는다.

1. `README.md`
2. `study/README.md`
3. stage README
4. 각 프로젝트의 `problem/README.md -> 구현 README -> docs/README.md -> notion/README.md`

## 핵심 커리큘럼

| 단계 | 프로젝트 | 문제 질문 | 내가 만든 답 | 검증 명령 | 상태 |
| --- | --- | --- | --- | --- | --- |
| foundations | [`01-navigation-patterns`](study/foundations/01-navigation-patterns/README.md) | Stack, Tab, Drawer, Deep Linking을 한 앱 안에서 어떻게 타입 안전하게 묶는가 | 중첩 navigator, custom header, badge, deep-link fallback을 갖춘 RN 파일럿 앱 | `make -C study/foundations/01-navigation-patterns/problem test`<br>`npm --prefix study/foundations/01-navigation-patterns/react-native run verify` | `verified` |
| foundations | [`02-virtualized-list-performance`](study/foundations/02-virtualized-list-performance/README.md) | 같은 10k 데이터셋에서 baseline과 optimized list 전략의 차이를 어떻게 측정하는가 | `FlatList` baseline과 `FlashList v2` optimized path를 비교하는 benchmark 앱 | `make -C study/foundations/02-virtualized-list-performance/problem benchmark` | `verified` |
| foundations | [`03-gestures-and-reanimated`](study/foundations/03-gestures-and-reanimated/README.md) | JS thread 개입 없이 제스처와 애니메이션 상호작용을 어떻게 설계하는가 | swipe card, reorder list, shared transition을 묶은 Reanimated 학습 앱 | `make -C study/foundations/03-gestures-and-reanimated/problem app-test` | `verified` |
| architecture | [`01-bridge-vs-jsi`](study/architecture/01-bridge-vs-jsi/README.md) | async serialized surface와 sync direct-call surface의 비용 차이는 어떻게 비교하는가 | RN 0.84 기준 benchmark 대시보드와 JSON export를 갖춘 비교 앱 | `make -C study/architecture/01-bridge-vs-jsi/problem app-test` | `verified` |
| architecture | [`02-native-modules`](study/architecture/02-native-modules/README.md) | JS/native 경계를 spec, codegen, consumer app으로 어떻게 설명하는가 | Battery, Haptics, Sensor 모듈 spec과 consumer screen을 묶은 boundary 예제 | `make -C study/architecture/02-native-modules/problem codegen` | `verified` |
| product-systems | [`01-offline-sync-foundations`](study/product-systems/01-offline-sync-foundations/README.md) | outbox, retry, DLQ, idempotency를 제품 앱 전에 어떻게 분리 학습하는가 | deterministic fake sync service와 queue/replay 규칙을 갖춘 브리지 프로젝트 | `make -C study/product-systems/01-offline-sync-foundations/problem app-test` | `verified` |
| product-systems | [`02-realtime-chat`](study/product-systems/02-realtime-chat/README.md) | offline send, ack reconcile, replay, presence를 local-first 모델로 어떻게 묶는가 | pending message와 replay-safe sync를 갖춘 채팅 앱 | `make -C study/product-systems/02-realtime-chat/problem app-test` | `verified` |
| product-systems | [`03-app-distribution`](study/product-systems/03-app-distribution/README.md) | 동작하는 제품 앱을 release rehearsal 단계까지 어떻게 끌고 가는가 | env separation, Fastlane, GitHub Actions, local rehearsal을 갖춘 배포 리허설 | `make -C study/product-systems/03-app-distribution/problem release-rehearsal` | `verified` |
| capstone | [`01-incident-ops-mobile`](study/capstone/01-incident-ops-mobile/README.md) | 모바일 클라이언트가 shared contract를 정확히 해석한다는 것을 어떻게 증명하는가 | DTO contract, Node backend, RN harness를 묶은 system/contract capstone | `make -C study/capstone/01-incident-ops-mobile/problem demo-e2e` | `verified` |
| capstone | [`02-incident-ops-mobile-client`](study/capstone/02-incident-ops-mobile-client/README.md) | 같은 incident domain을 hiring-facing RN 완성작으로 어떻게 다시 구현하는가 | auth, feed, role action, persistent outbox, demo flow를 갖춘 최종 클라이언트 | `make -C study/capstone/02-incident-ops-mobile-client/problem demo-e2e` | `verified` |

## 검증 시작점

저장소 공통 검증은 아래 세 스크립트를 기준으로 본다.

```bash
bash scripts/check_study_docs.sh
bash scripts/verify_study_structure.sh
bash scripts/report_study_status.sh
```

각 프로젝트의 세부 검증 명령은 해당 프로젝트 README와 `problem/README.md`를 따른다.

## 의도적으로 범위 밖

- Expo managed workflow 중심 저장소로 재구성하지 않는다.
- App Store / Play Store 실제 업로드나 signing secret 보관소로 쓰지 않는다.
- `docs/`를 장문 작업 로그로 쓰지 않는다.
- `notion/`을 숨기지 않지만, 메인 답안 본문으로도 쓰지 않는다.

## 참고 문서

- [study/README.md](study/README.md)
- [docs/README.md](docs/README.md)
- [docs/curriculum-map.md](docs/curriculum-map.md)
- [docs/path-migration-map.md](docs/path-migration-map.md)
