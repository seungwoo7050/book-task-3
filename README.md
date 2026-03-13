# book-task-3

이 저장소는 여러 개발 학습 프로젝트를 모아 둔 아카이브이지만, 루트 README의 역할은 단순 카탈로그가 아닙니다. 이 문서는 `무슨 폴더가 있는가`보다 `어떤 프로젝트를 어떤 순서로 밟을 것인가`를 먼저 안내하는 학습 루트 문서입니다.

그래서 루트/트랙 README보다 `개별 프로젝트 README`를 직접 연결하는 방식을 기본으로 삼습니다. 한 저장소를 처음부터 끝까지 전부 읽기보다, 필요한 노드만 순서대로 밟아 가는 쪽이 이 문서의 기본 사용법입니다.

## 이 문서를 읽는 법

| 표기 | 뜻 |
| --- | --- |
| `base` | 가장 먼저 밟는 기초 노드 |
| `shared` | 여러 직무가 함께 쓰는 중간 노드 |
| `branch` | 특정 직무로 갈라지는 노드 |
| `capstone` | 대표 결과물 노드 |

기본 규칙은 아래 네 줄로 요약됩니다.

1. 먼저 `최소 공통 루트`를 밟습니다.
2. `backend / game / system-heavy` 쪽이면 `서버 공통 심화 루트`를 선택적으로 추가합니다.
3. 그다음 원하는 직무의 `핵심 루트`로 들어갑니다.
4. 시간이 충분하면 같은 직무의 `전체 주행 루트`를 따라갑니다.

예외도 분명합니다.

- 게임 서버는 [Web Server](network-atda/study/01-Application-Protocols-and-Sockets/web-server/README.md) 이후 바로 분기해도 됩니다.
- Frontend와 Mobile은 보통 `서버 공통 심화 루트`를 요구하지 않습니다.

이 문서의 메인 링크는 모두 `프로젝트 README`로 직접 연결합니다. 루트/트랙 README는 마지막 `보조 카탈로그`에서만 묶어 둡니다.

현재 커버리지는 학습용 핵심 루트로는 이미 충분한 편입니다. 새 프로젝트는 기존 프로젝트와 학습 포인트가 크게 겹치지 않고, 뚜렷한 공백을 메울 때만 추가합니다.

## 전체 노드 트리

| 그룹 | 누가 주로 보는가 | 역할 | 노드 시퀀스 |
| --- | --- | --- | --- |
| Common Spine | 전 직무 공통 | `base -> shared -> shared` | [Web Server](network-atda/study/01-Application-Protocols-and-Sockets/web-server/README.md) -> [02-http-and-api-basics](backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/README.md) -> [03-networked-ui-patterns](front-react/study/frontend-foundations/03-networked-ui-patterns/README.md) |
| Server Deep - Core | 웹 백엔드, 게임 서버, 시스템 지향 | `shared -> shared -> shared -> shared` | [shlab](cs-core/study/Systems-Programming/shlab/README.md) -> [proxylab](cs-core/study/Systems-Programming/proxylab/README.md) -> [03-mini-lsm-store](database-systems/go/database-internals/projects/03-mini-lsm-store/README.md) -> [08-btree-index-and-query-scan](database-systems/go/database-internals/projects/08-btree-index-and-query-scan/README.md) |
| Server Deep - Extended | 더 깊은 서버/시스템 심화 | `shared -> shared -> shared -> shared -> shared -> capstone` | [shlab](cs-core/study/Systems-Programming/shlab/README.md) -> [malloclab](cs-core/study/Systems-Programming/malloclab/README.md) -> [proxylab](cs-core/study/Systems-Programming/proxylab/README.md) -> [03-mini-lsm-store](database-systems/go/database-internals/projects/03-mini-lsm-store/README.md) -> [08-btree-index-and-query-scan](database-systems/go/database-internals/projects/08-btree-index-and-query-scan/README.md) -> [05-clustered-kv-capstone](database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/README.md) |
| Backend Spring | Spring 기반 백엔드 | `branch -> ... -> capstone` | [A-auth-lab](backend-spring/labs/A-auth-lab/README.md) -> [C-authorization-lab](backend-spring/labs/C-authorization-lab/README.md) -> [D-data-jpa-lab](backend-spring/labs/D-data-jpa-lab/README.md) -> [G-ops-observability-lab](backend-spring/labs/G-ops-observability-lab/README.md) -> [commerce-backend](backend-spring/capstone/commerce-backend/README.md) -> [commerce-backend-v2](backend-spring/capstone/commerce-backend-v2/README.md) |
| Backend FastAPI | Python API 백엔드 | `branch -> ... -> capstone` | [A-auth-lab](backend-fastapi/labs/A-auth-lab/README.md) -> [D-data-api-lab](backend-fastapi/labs/D-data-api-lab/README.md) -> [E-async-jobs-lab](backend-fastapi/labs/E-async-jobs-lab/README.md) -> [F-realtime-lab](backend-fastapi/labs/F-realtime-lab/README.md) -> [workspace-backend](backend-fastapi/capstone/workspace-backend/README.md) -> [workspace-backend-v2-msa](backend-fastapi/capstone/workspace-backend-v2-msa/README.md) |
| Backend Node / NestJS | Node/Nest 기반 백엔드 | `branch -> ... -> capstone` | [03-rest-api-foundations](backend-node/study/Node-Backend-Architecture/core/03-rest-api-foundations/README.md) -> [05-auth-and-authorization](backend-node/study/Node-Backend-Architecture/core/05-auth-and-authorization/README.md) -> [06-persistence-and-repositories](backend-node/study/Node-Backend-Architecture/core/06-persistence-and-repositories/README.md) -> [08-production-readiness](backend-node/study/Node-Backend-Architecture/applied/08-production-readiness/README.md) -> [09-platform-capstone](backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/README.md) -> [10-shippable-backend-service](backend-node/study/Node-Backend-Architecture/applied/10-shippable-backend-service/README.md) |
| Frontend | 웹 프론트엔드 | `branch -> ... -> capstone` | [01-semantic-layouts-and-a11y](front-react/study/frontend-foundations/01-semantic-layouts-and-a11y/README.md) -> [02-dom-state-and-events](front-react/study/frontend-foundations/02-dom-state-and-events/README.md) -> [03-networked-ui-patterns](front-react/study/frontend-foundations/03-networked-ui-patterns/README.md) -> [03-hooks-and-events](front-react/study/react-internals/03-hooks-and-events/README.md) -> [04-runtime-demo-app](front-react/study/react-internals/04-runtime-demo-app/README.md) -> [01-ops-triage-console](front-react/study/frontend-portfolio/01-ops-triage-console/README.md) -> [03-realtime-collab-workspace](front-react/study/frontend-portfolio/03-realtime-collab-workspace/README.md) |
| Game Server | 실시간 서버 / authoritative simulation | `branch -> ... -> capstone` | [Web Server](network-atda/study/01-Application-Protocols-and-Sockets/web-server/README.md) -> [RDT Protocol](network-atda/study/02-Reliable-Transport/rdt-protocol/README.md) -> [01-eventlab](cpp-server/study/shared-core/01-eventlab/README.md) -> [02-msglab](cpp-server/study/shared-core/02-msglab/README.md) -> [01-ticklab](cpp-server/study/game-track/01-ticklab/README.md) -> [02-rollbacklab](cpp-server/study/game-track/02-rollbacklab/README.md) -> [03-arenaserv](cpp-server/study/game-track/03-arenaserv/README.md) |
| Mobile | React Native / 모바일 클라이언트 | `branch -> ... -> capstone` | [01-navigation-patterns](mobile/study/foundations/01-navigation-patterns/README.md) -> [02-native-modules](mobile/study/architecture/02-native-modules/README.md) -> [01-offline-sync-foundations](mobile/study/product-systems/01-offline-sync-foundations/README.md) -> [02-realtime-chat](mobile/study/product-systems/02-realtime-chat/README.md) -> [02-incident-ops-mobile-client](mobile/study/capstone/02-incident-ops-mobile-client/README.md) |

## 최소 공통 루트

모든 사람이 같은 커리큘럼을 길게 밟을 필요는 없습니다. 루트 README 기준 공통 바닥은 아래 세 노드로 고정합니다.

1. `base` [Web Server](network-atda/study/01-Application-Protocols-and-Sockets/web-server/README.md)
2. `shared` [02-http-and-api-basics](backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/README.md)
3. `shared` [03-networked-ui-patterns](front-react/study/frontend-foundations/03-networked-ui-patterns/README.md)

이 세 노드는 서로 다른 직무가 만나도 같은 단어로 대화할 수 있게 만드는 공통 바닥입니다.

- 요청과 응답이 wire 위에서 어떻게 오가는가
- framework 이전의 API 표면이 어떻게 생기는가
- 클라이언트가 loading, error, retry를 어떻게 받아들이는가

게임 서버를 목표로 한다면 이 세 노드를 모두 끝낼 필요는 없습니다. [Web Server](network-atda/study/01-Application-Protocols-and-Sockets/web-server/README.md) 이후 바로 게임 서버 분기로 넘어가도 괜찮습니다.

## 서버 공통 심화 루트

이 섹션은 전원 필수가 아니라 `backend / game / system-heavy` 지향 공통 심화입니다. Frontend와 Mobile은 보통 여기까지 요구하지 않습니다.

중요한 점은 여기서도 `cs-core` 전체를 필수로 요구하지 않는다는 것입니다. 이 루트는 서버 구현에 직접 연결되는 일부 프로젝트만 발췌한 선택 심화 경로입니다.

서버 직무에서 최소로 보는 일부 노드는 현재 문서 기준으로 아래처럼 고정합니다.

| 범주 | 최소로 보는 일부 노드 | 비고 |
| --- | --- | --- |
| `cs-core` | [shlab](cs-core/study/Systems-Programming/shlab/README.md), [proxylab](cs-core/study/Systems-Programming/proxylab/README.md) | `malloclab`은 확장 루트에만 둡니다. |
| `network-atda` - web backend minimum | [Web Server](network-atda/study/01-Application-Protocols-and-Sockets/web-server/README.md) | 웹 백엔드는 네트워크 전체보다 HTTP 요청/응답 표면을 먼저 익히는 쪽을 기본으로 둡니다. |
| `network-atda` - game server minimum | [Web Server](network-atda/study/01-Application-Protocols-and-Sockets/web-server/README.md), [RDT Protocol](network-atda/study/02-Reliable-Transport/rdt-protocol/README.md) | 게임 서버 핵심 루트의 최소 네트워크 시작점입니다. |
| `network-atda` - game server extended | [UDP Pinger](network-atda/study/01-Application-Protocols-and-Sockets/udp-pinger/README.md), [Web Proxy](network-atda/study/01-Application-Protocols-and-Sockets/web-proxy/README.md), [Selective Repeat](network-atda/study/02-Reliable-Transport/selective-repeat/README.md), [ICMP Pinger](network-atda/study/04-Network-Diagnostics-and-Routing/icmp-pinger/README.md), [Traceroute](network-atda/study/04-Network-Diagnostics-and-Routing/traceroute/README.md), [Routing](network-atda/study/04-Network-Diagnostics-and-Routing/routing/README.md) | 전체 주행 루트에서만 붙입니다. |

현재 루트 README 기준으로는 위 구성이 기본 결정안입니다. 지금 당장 공통 필수에 더 추가하거나 뺄 프로젝트는 없고, 새 프로젝트가 생기더라도 `최소 루트`가 아니라 `확장 루트`에 먼저 들어가는 쪽을 기본 원칙으로 삼습니다.

### 핵심

1. `shared` [shlab](cs-core/study/Systems-Programming/shlab/README.md)
2. `shared` [proxylab](cs-core/study/Systems-Programming/proxylab/README.md)
3. `shared` [03-mini-lsm-store](database-systems/go/database-internals/projects/03-mini-lsm-store/README.md)
4. `shared` [08-btree-index-and-query-scan](database-systems/go/database-internals/projects/08-btree-index-and-query-scan/README.md)

### 확장

1. `shared` [shlab](cs-core/study/Systems-Programming/shlab/README.md)
2. `shared` [malloclab](cs-core/study/Systems-Programming/malloclab/README.md)
3. `shared` [proxylab](cs-core/study/Systems-Programming/proxylab/README.md)
4. `shared` [03-mini-lsm-store](database-systems/go/database-internals/projects/03-mini-lsm-store/README.md)
5. `shared` [08-btree-index-and-query-scan](database-systems/go/database-internals/projects/08-btree-index-and-query-scan/README.md)
6. `capstone` [05-clustered-kv-capstone](database-systems/go/ddia-distributed-systems/projects/05-clustered-kv-capstone/README.md)

## 직무별 핵심 루트

Backend 루트를 읽을 때의 짧은 기준:

여기서 `WAS`는 특정 프레임워크 이름이 아니라, HTTP 요청을 받아 비즈니스 로직을 실행하고 DB와 연결하고 API를 반환하는 애플리케이션 서버 층을 뜻합니다. 이 레포에서는 Spring, FastAPI, Node 트랙이 그 역할을 나눠 맡습니다.

### Backend - Spring

1. `branch` [A-auth-lab](backend-spring/labs/A-auth-lab/README.md)
2. `branch` [C-authorization-lab](backend-spring/labs/C-authorization-lab/README.md)
3. `branch` [D-data-jpa-lab](backend-spring/labs/D-data-jpa-lab/README.md)
4. `branch` [G-ops-observability-lab](backend-spring/labs/G-ops-observability-lab/README.md)
5. `capstone` [commerce-backend](backend-spring/capstone/commerce-backend/README.md)
6. `capstone` [commerce-backend-v2](backend-spring/capstone/commerce-backend-v2/README.md)

### Backend - FastAPI

1. `branch` [A-auth-lab](backend-fastapi/labs/A-auth-lab/README.md)
2. `branch` [D-data-api-lab](backend-fastapi/labs/D-data-api-lab/README.md)
3. `branch` [E-async-jobs-lab](backend-fastapi/labs/E-async-jobs-lab/README.md)
4. `branch` [F-realtime-lab](backend-fastapi/labs/F-realtime-lab/README.md)
5. `capstone` [workspace-backend](backend-fastapi/capstone/workspace-backend/README.md)
6. `capstone` [workspace-backend-v2-msa](backend-fastapi/capstone/workspace-backend-v2-msa/README.md)

### Backend - Node / NestJS

1. `branch` [03-rest-api-foundations](backend-node/study/Node-Backend-Architecture/core/03-rest-api-foundations/README.md)
2. `branch` [05-auth-and-authorization](backend-node/study/Node-Backend-Architecture/core/05-auth-and-authorization/README.md)
3. `branch` [06-persistence-and-repositories](backend-node/study/Node-Backend-Architecture/core/06-persistence-and-repositories/README.md)
4. `branch` [08-production-readiness](backend-node/study/Node-Backend-Architecture/applied/08-production-readiness/README.md)
5. `capstone` [09-platform-capstone](backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/README.md)
6. `capstone` [10-shippable-backend-service](backend-node/study/Node-Backend-Architecture/applied/10-shippable-backend-service/README.md)

### Frontend

1. `branch` [01-semantic-layouts-and-a11y](front-react/study/frontend-foundations/01-semantic-layouts-and-a11y/README.md)
2. `branch` [02-dom-state-and-events](front-react/study/frontend-foundations/02-dom-state-and-events/README.md)
3. `branch` [03-networked-ui-patterns](front-react/study/frontend-foundations/03-networked-ui-patterns/README.md)
4. `branch` [03-hooks-and-events](front-react/study/react-internals/03-hooks-and-events/README.md)
5. `branch` [04-runtime-demo-app](front-react/study/react-internals/04-runtime-demo-app/README.md)
6. `branch` [01-ops-triage-console](front-react/study/frontend-portfolio/01-ops-triage-console/README.md)
7. `capstone` [03-realtime-collab-workspace](front-react/study/frontend-portfolio/03-realtime-collab-workspace/README.md)

### Game Server

1. `base` [Web Server](network-atda/study/01-Application-Protocols-and-Sockets/web-server/README.md)
2. `branch` [RDT Protocol](network-atda/study/02-Reliable-Transport/rdt-protocol/README.md)
3. `branch` [01-eventlab](cpp-server/study/shared-core/01-eventlab/README.md)
4. `branch` [02-msglab](cpp-server/study/shared-core/02-msglab/README.md)
5. `branch` [01-ticklab](cpp-server/study/game-track/01-ticklab/README.md)
6. `branch` [02-rollbacklab](cpp-server/study/game-track/02-rollbacklab/README.md)
7. `capstone` [03-arenaserv](cpp-server/study/game-track/03-arenaserv/README.md)

### Mobile

1. `branch` [01-navigation-patterns](mobile/study/foundations/01-navigation-patterns/README.md)
2. `branch` [02-native-modules](mobile/study/architecture/02-native-modules/README.md)
3. `branch` [01-offline-sync-foundations](mobile/study/product-systems/01-offline-sync-foundations/README.md)
4. `branch` [02-realtime-chat](mobile/study/product-systems/02-realtime-chat/README.md)
5. `capstone` [02-incident-ops-mobile-client](mobile/study/capstone/02-incident-ops-mobile-client/README.md)

## 직무별 전체 주행 루트

### Spring Full

[A-auth-lab](backend-spring/labs/A-auth-lab/README.md) -> [B-federation-security-lab](backend-spring/labs/B-federation-security-lab/README.md) -> [C-authorization-lab](backend-spring/labs/C-authorization-lab/README.md) -> [D-data-jpa-lab](backend-spring/labs/D-data-jpa-lab/README.md) -> [E-event-messaging-lab](backend-spring/labs/E-event-messaging-lab/README.md) -> [F-cache-concurrency-lab](backend-spring/labs/F-cache-concurrency-lab/README.md) -> [G-ops-observability-lab](backend-spring/labs/G-ops-observability-lab/README.md) -> [commerce-backend](backend-spring/capstone/commerce-backend/README.md) -> [commerce-backend-v2](backend-spring/capstone/commerce-backend-v2/README.md)

### FastAPI Full

[A-auth-lab](backend-fastapi/labs/A-auth-lab/README.md) -> [B-federation-security-lab](backend-fastapi/labs/B-federation-security-lab/README.md) -> [C-authorization-lab](backend-fastapi/labs/C-authorization-lab/README.md) -> [D-data-api-lab](backend-fastapi/labs/D-data-api-lab/README.md) -> [E-async-jobs-lab](backend-fastapi/labs/E-async-jobs-lab/README.md) -> [F-realtime-lab](backend-fastapi/labs/F-realtime-lab/README.md) -> [G-ops-lab](backend-fastapi/labs/G-ops-lab/README.md) -> [workspace-backend](backend-fastapi/capstone/workspace-backend/README.md) -> [H-service-boundary-lab](backend-fastapi/labs/H-service-boundary-lab/README.md) -> [I-event-integration-lab](backend-fastapi/labs/I-event-integration-lab/README.md) -> [J-edge-gateway-lab](backend-fastapi/labs/J-edge-gateway-lab/README.md) -> [K-distributed-ops-lab](backend-fastapi/labs/K-distributed-ops-lab/README.md) -> [workspace-backend-v2-msa](backend-fastapi/capstone/workspace-backend-v2-msa/README.md)

### Node Full

[00-language-and-typescript](backend-node/study/Node-Backend-Architecture/bridge/00-language-and-typescript/README.md) -> [01-node-runtime-and-tooling](backend-node/study/Node-Backend-Architecture/bridge/01-node-runtime-and-tooling/README.md) -> [02-http-and-api-basics](backend-node/study/Node-Backend-Architecture/bridge/02-http-and-api-basics/README.md) -> [03-rest-api-foundations](backend-node/study/Node-Backend-Architecture/core/03-rest-api-foundations/README.md) -> [04-request-pipeline](backend-node/study/Node-Backend-Architecture/core/04-request-pipeline/README.md) -> [05-auth-and-authorization](backend-node/study/Node-Backend-Architecture/core/05-auth-and-authorization/README.md) -> [06-persistence-and-repositories](backend-node/study/Node-Backend-Architecture/core/06-persistence-and-repositories/README.md) -> [07-domain-events](backend-node/study/Node-Backend-Architecture/core/07-domain-events/README.md) -> [08-production-readiness](backend-node/study/Node-Backend-Architecture/applied/08-production-readiness/README.md) -> [09-platform-capstone](backend-node/study/Node-Backend-Architecture/applied/09-platform-capstone/README.md) -> [10-shippable-backend-service](backend-node/study/Node-Backend-Architecture/applied/10-shippable-backend-service/README.md)

### Frontend Full

[01-semantic-layouts-and-a11y](front-react/study/frontend-foundations/01-semantic-layouts-and-a11y/README.md) -> [02-dom-state-and-events](front-react/study/frontend-foundations/02-dom-state-and-events/README.md) -> [03-networked-ui-patterns](front-react/study/frontend-foundations/03-networked-ui-patterns/README.md) -> [01-vdom-foundations](front-react/study/react-internals/01-vdom-foundations/README.md) -> [02-render-pipeline](front-react/study/react-internals/02-render-pipeline/README.md) -> [03-hooks-and-events](front-react/study/react-internals/03-hooks-and-events/README.md) -> [04-runtime-demo-app](front-react/study/react-internals/04-runtime-demo-app/README.md) -> [01-ops-triage-console](front-react/study/frontend-portfolio/01-ops-triage-console/README.md) -> [02-client-onboarding-portal](front-react/study/frontend-portfolio/02-client-onboarding-portal/README.md) -> [03-realtime-collab-workspace](front-react/study/frontend-portfolio/03-realtime-collab-workspace/README.md)

### Game Extended

[Web Server](network-atda/study/01-Application-Protocols-and-Sockets/web-server/README.md) -> [UDP Pinger](network-atda/study/01-Application-Protocols-and-Sockets/udp-pinger/README.md) -> [Web Proxy](network-atda/study/01-Application-Protocols-and-Sockets/web-proxy/README.md) -> [RDT Protocol](network-atda/study/02-Reliable-Transport/rdt-protocol/README.md) -> [Selective Repeat](network-atda/study/02-Reliable-Transport/selective-repeat/README.md) -> [ICMP Pinger](network-atda/study/04-Network-Diagnostics-and-Routing/icmp-pinger/README.md) -> [Traceroute](network-atda/study/04-Network-Diagnostics-and-Routing/traceroute/README.md) -> [Routing](network-atda/study/04-Network-Diagnostics-and-Routing/routing/README.md) -> [01-eventlab](cpp-server/study/shared-core/01-eventlab/README.md) -> [02-msglab](cpp-server/study/shared-core/02-msglab/README.md) -> [01-ticklab](cpp-server/study/game-track/01-ticklab/README.md) -> [02-rollbacklab](cpp-server/study/game-track/02-rollbacklab/README.md) -> [03-arenaserv](cpp-server/study/game-track/03-arenaserv/README.md) -> [Tactical Arena Server](network-atda/study/05-Game-Server-Capstone/tactical-arena-server/README.md)

### Mobile Full

[01-navigation-patterns](mobile/study/foundations/01-navigation-patterns/README.md) -> [02-virtualized-list-performance](mobile/study/foundations/02-virtualized-list-performance/README.md) -> [03-gestures-and-reanimated](mobile/study/foundations/03-gestures-and-reanimated/README.md) -> [01-bridge-vs-jsi](mobile/study/architecture/01-bridge-vs-jsi/README.md) -> [02-native-modules](mobile/study/architecture/02-native-modules/README.md) -> [01-offline-sync-foundations](mobile/study/product-systems/01-offline-sync-foundations/README.md) -> [02-realtime-chat](mobile/study/product-systems/02-realtime-chat/README.md) -> [03-app-distribution](mobile/study/product-systems/03-app-distribution/README.md) -> [01-incident-ops-mobile](mobile/study/capstone/01-incident-ops-mobile/README.md) -> [02-incident-ops-mobile-client](mobile/study/capstone/02-incident-ops-mobile-client/README.md)

## 보조 카탈로그

프로젝트 노드보다 상위 문서부터 보고 싶을 때만 아래 루트 README로 이동합니다.

- [network-atda](network-atda/README.md)
- [database-systems](database-systems/README.md)
- [backend-spring](backend-spring/README.md)
- [backend-fastapi](backend-fastapi/README.md)
- [backend-node](backend-node/README.md)
- [front-react](front-react/README.md)
- [mobile](mobile/README.md)
- [cpp-server](cpp-server/README.md)
- [cs-core](cs-core/README.md)
- [algorithm](algorithm/README.md)
