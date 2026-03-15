# mobile 종합 과제 답안지

이 문서는 모바일 capstone을 실제 contract, backend, React Native source만으로 해설하는 답안지다. 두 항목 모두 shared contract를 어디에 두고, 화면 모델과 서버 검증을 어떻게 맞물리게 만드는지가 핵심이다.

| lab | 해답 요약 | 검증 |
| --- | --- | --- |
| [01-incident-ops-mobile-node-server](01-incident-ops-mobile-node-server_answer.md) | incident-ops backend와 shared DTO contract를 canonical source로 유지하고, React Native harness가 그 계약을 올바르게 해석한다는 사실을 증명하는 capstone 과제다. 핵심은 OfflineQueueEngine와 assertOk, login 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test && make app-build && make app-test && make server-test && make demo-e2e` |
| [01-incident-ops-mobile-react-native](01-incident-ops-mobile-react-native_answer.md) | incident-ops backend와 shared DTO contract를 canonical source로 유지하고, React Native harness가 그 계약을 올바르게 해석한다는 사실을 증명하는 capstone 과제다. 핵심은 initialIncident와 initialApproval, initialAuditLogs 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test && make app-build && make app-test && make server-test && make demo-e2e` |
| [02-incident-ops-mobile-client-node-server](02-incident-ops-mobile-client-node-server_answer.md) | 기존 incident-ops domain과 shared contract를 유지한 채, 실제 화면 흐름, 오프라인 복구, replay-safe realtime behavior를 갖춘 hiring-facing RN 클라이언트를 완성하는 과제다. 핵심은 main와 OfflineQueueEngine, assertOk 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test && make app-build && make app-test && make server-test && make demo-e2e` |
| [02-incident-ops-mobile-client-react-native](02-incident-ops-mobile-client-react-native_answer.md) | 기존 incident-ops domain과 shared contract를 유지한 채, 실제 화면 흐름, 오프라인 복구, replay-safe realtime behavior를 갖춘 hiring-facing RN 클라이언트를 완성하는 과제다. 핵심은 AppModelContext와 createId, defaultConnectionState 흐름을 구현하고 테스트를 통과시키는 것이다. | `make test && make app-build && make app-test && make server-test && make demo-e2e` |

## 읽는 방법

각 행은 실제 lab 답안지로 직접 연결된다. 상세 해설은 각 leaf `_answer.md`에서 확인한다.
