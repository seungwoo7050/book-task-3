# mobile 비필수 답안지

이 문서는 모바일 심화 과제를 source-first로 해설하는 답안지다. 핵심은 아키텍처 경계와 release discipline을 실제 파일 구조와 테스트 구조로 설명하는 것이다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [01-bridge-vs-jsi-react-native](01-bridge-vs-jsi-react-native_answer.md) | RN 0.84 기준으로 runtime 자체를 토글하는 대신, Promise + serialized payload 표면과 sync direct-call 표면을 같은 workload로 비교하는 benchmark를 만든다. 핵심은 RUNS와 computeStats, buildExport 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test && make app-build && make app-test` |
| [02-native-modules-react-native](02-native-modules-react-native_answer.md) | Battery, Haptics, Sensor 세 모듈의 TypeScript public spec을 고정하고, codegen summary와 consumer app을 통해 JS/native 경계를 설명하는 과제다. 핵심은 NativeModulesStudyApp와 styles, MODULE_SPECS 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test && make codegen && make app-build && make app-test` |
| [03-app-distribution-react-native](03-app-distribution-react-native_answer.md) | 검증된 realtime-chat snapshot을 release candidate로 가져와, 실제 credential을 저장소에 넣지 않고도 packaging, env separation, automation rehearsal을 증명하는 과제다. 핵심은 createPendingMessage와 reconcileAck, applyReplayEvents 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test && make app-build && make app-test && make release-rehearsal` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
