# mobile 종합 과제 문제지

`mobile` capstone은 foundations와 architecture, product-systems에서 나눠 익힌 문제를 하나의 incident 도메인 안에서 다시 묶게 만드는 종합 과제입니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [01-incident-ops-mobile-node-server](01-incident-ops-mobile-node-server.md) | incident-ops backend와 shared DTO contract를 canonical source로 유지하고, React Native harness가 그 계약을 올바르게 해석한다는 사실을 증명하는 capstone 과제다. | `make test && make app-build && make app-test && make server-test && make demo-e2e` |
| [01-incident-ops-mobile-react-native](01-incident-ops-mobile-react-native.md) | incident-ops backend와 shared DTO contract를 canonical source로 유지하고, React Native harness가 그 계약을 올바르게 해석한다는 사실을 증명하는 capstone 과제다. | `make test && make app-build && make app-test && make server-test && make demo-e2e` |
| [02-incident-ops-mobile-client-node-server](02-incident-ops-mobile-client-node-server.md) | 기존 incident-ops domain과 shared contract를 유지한 채, 실제 화면 흐름, 오프라인 복구, replay-safe realtime behavior를 갖춘 hiring-facing RN 클라이언트를 완성하는 과제다. | `make test && make app-build && make app-test && make server-test && make demo-e2e` |
| [02-incident-ops-mobile-client-react-native](02-incident-ops-mobile-client-react-native.md) | 기존 incident-ops domain과 shared contract를 유지한 채, 실제 화면 흐름, 오프라인 복구, replay-safe realtime behavior를 갖춘 hiring-facing RN 클라이언트를 완성하는 과제다. | `make test && make app-build && make app-test && make server-test && make demo-e2e` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
