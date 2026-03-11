# FastAPI 백엔드 랩 커리큘럼

## 왜 이런 순서인가

이 저장소는 하나의 긴 튜토리얼이 아니라, 실무 FastAPI 백엔드에서 반복해서 만나는 문제를 단계별 랩으로 쪼개 놓은 코스입니다. 순서를 정한 기준은 "앞 랩의 개념이 다음 랩의 전제지식이 되느냐"와 "학생이 자신의 포트폴리오로 옮겨 갈 때 어떤 설명 흐름이 자연스러우냐"입니다.

## 트랙 구분 기준

- 필수 트랙은 단일 FastAPI 백엔드를 설계, 검증, 문서화하는 기준선입니다.
- 심화 트랙은 같은 도메인을 MSA로 분해할 때 새로 생기는 경계, 이벤트, gateway, 분산 운영 문제를 다룹니다.
- 시간이 부족하면 필수 트랙을 먼저 끝내고, 심화 트랙은 이후 별도 학습 단계로 가져가는 편이 자연스럽습니다.

## 단계별 추천 경로

### 필수 트랙

1. [A-auth-lab](../labs/A-auth-lab/README.md)
2. [B-federation-security-lab](../labs/B-federation-security-lab/README.md)
3. [C-authorization-lab](../labs/C-authorization-lab/README.md)
4. [D-data-api-lab](../labs/D-data-api-lab/README.md)
5. [E-async-jobs-lab](../labs/E-async-jobs-lab/README.md)
6. [F-realtime-lab](../labs/F-realtime-lab/README.md)
7. [G-ops-lab](../labs/G-ops-lab/README.md)
8. [capstone/workspace-backend](../capstone/workspace-backend/README.md)

### 심화 트랙

- 진입 기준: `workspace-backend`까지 읽고 실행해 본 뒤, 인증/인가/데이터 API/비동기/실시간/운영성을 단일 백엔드 기준으로 설명할 수 있어야 합니다.

1. [H-service-boundary-lab](../labs/H-service-boundary-lab/README.md)
2. [I-event-integration-lab](../labs/I-event-integration-lab/README.md)
3. [J-edge-gateway-lab](../labs/J-edge-gateway-lab/README.md)
4. [K-distributed-ops-lab](../labs/K-distributed-ops-lab/README.md)
5. [capstone/workspace-backend-v2-msa](../capstone/workspace-backend-v2-msa/README.md)

## 전체 추천 순서

`A -> B -> C -> D -> E -> F -> G -> workspace-backend -> H -> I -> J -> K -> workspace-backend-v2-msa`

## 랩별 학습 포인트

### 필수 트랙

#### A-auth-lab

- 로컬 회원가입, 로그인, 이메일 검증, 비밀번호 재설정
- Argon2 해시, refresh token rotation, cookie + CSRF 조합
- "사용자 인증 흐름을 어떻게 끊김 없이 설명할 것인가"를 배우는 시작점

#### B-federation-security-lab

- Google OIDC 로그인, 외부 계정 연결
- TOTP 기반 2FA, recovery code, 로그인 throttling, 감사 로그
- 로컬 인증 이후 어떤 보안 강화를 붙여야 하는지 보여 주는 랩

#### C-authorization-lab

- 워크스페이스 생성, 초대, 역할 변경
- owner/admin/member/viewer 경계와 소유권 규칙
- 인증과 인가를 분리해 설명하는 훈련에 적합한 랩

#### D-data-api-lab

- 프로젝트, 태스크, 댓글 CRUD
- 필터링, 정렬, 페이지네이션, 소프트 삭제
- 낙관적 락과 서비스 계층 경계처럼 데이터 중심 설계의 기본기를 다룸

#### E-async-jobs-lab

- Redis + Celery 기반 비동기 작업 실행
- outbox handoff, retry 상태 전이, idempotency key
- "요청은 빨리 끝내고, 실제 처리는 안전하게 뒤로 미루는" 설계를 배우는 랩

#### F-realtime-lab

- WebSocket 인증
- presence heartbeat와 TTL
- 여러 활성 소켓으로 fan-out 하는 기본 모델
- 실시간 통신을 데이터 저장소나 권한 문제와 섞지 않고 따로 이해하게 돕는 랩

#### G-ops-lab

- liveness/readiness 구분
- 구조화 로그와 최소 metrics surface
- CI 기대치와 AWS target shape 문서
- 운영성을 "인프라 자동화"가 아니라 "설명 가능한 실행 기준"으로 정리하는 랩

#### workspace-backend

- 인증, 인가, 데이터 API, 알림 큐, 실시간 전달을 하나의 협업형 백엔드로 통합
- 앞선 랩의 코드를 재사용하는 대신, 개념을 다시 조합해 제품형 구조를 만든다

### 심화 트랙

#### H-service-boundary-lab

- `identity-service`와 `workspace-service` 분리
- 서비스별 DB ownership과 bearer claims 기반 사용자 전달
- "같은 도메인을 어디서 쪼개는가"를 처음으로 설명하는 랩

#### I-event-integration-lab

- `workspace-service` outbox와 `notification-service` consumer
- Redis Streams와 idempotent consumer
- 동기 API와 비동기 전달을 서비스 간 통합으로 확장

#### J-edge-gateway-lab

- public API를 gateway에 유지하고 내부 서비스로 fan-out
- cookie + CSRF는 edge에만 두고 내부는 bearer only
- request id를 생성해 내부 호출 전체로 전달

#### K-distributed-ops-lab

- 서비스별 live / ready 구분
- JSON 로그와 request id, 최소 metrics
- Compose health matrix와 AWS target shape 문서

#### workspace-backend-v2-msa

- 같은 협업형 도메인을 `gateway + identity-service + workspace-service + notification-service`로 재편
- 단일 백엔드 기준선과 MSA 재편을 같은 문제 정의 안에서 비교

## 이 커리큘럼이 학생에게 주는 이점

- 작은 범위에서 실패하고 다시 고치기 쉽습니다.
- 특정 주제를 면접이나 README에서 따로 설명하기 좋습니다.
- capstone에 들어가기 전에 "무엇을 왜 붙이는지"를 단계별로 정리할 수 있습니다.
- 이후 H~K 랩을 통해 단일 백엔드에서 MSA로 넘어갈 때 어떤 복잡성이 추가되는지도 별도로 설명할 수 있습니다.

## 포트폴리오로 확장할 때의 권장 방식

- 필수 트랙에서는 인증 모델, 데이터 경계, 비동기 경계, 운영 기준을 단일 백엔드 관점에서 먼저 정리합니다.
- 심화 트랙으로 넘어갈 때는 분해 이유, 이벤트 계약, request id 전파, 서비스별 운영 기준을 별도로 적습니다.
- A~G 랩 중 자신이 약한 주제를 하나 골라 별도 실험 랩으로 다시 만들어 봅니다.
- 각 프로젝트에서 "학습용 단순화"와 "실서비스로 가려면 필요한 추가 작업"을 분리해서 적습니다.
