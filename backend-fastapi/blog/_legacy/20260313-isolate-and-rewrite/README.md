# backend-fastapi blog

이 폴더는 `backend-fastapi`의 각 독립 프로젝트를 `blog-writing-guide.md` 기준으로 다시 쓴 source-first 블로그 시리즈입니다.

## 이 시리즈가 따르는 기준

- 근거는 `README`, `problem/README.md`, `fastapi/README.md`, `Makefile`, `compose.yaml`, `app/`, `tests/`, `contracts/README.md`, `git log/show`, `docs/verification-report.md`만 사용합니다.
- `notion/`과 `notion-archive/`는 읽지 않습니다.
- chronology는 커밋과 테스트 표면에서 복원하고, 비어 있는 부분은 일반적인 수준의 개발자라면 자연스럽게 관찰할 수 있는 범위에서만 보수적으로 추론합니다.
- 코드는 핵심만 남기고, CLI는 재실행 경로가 보이게 정리합니다.

## 필수 트랙

1. [A-auth-lab](labs/A-auth-lab/00-series-map.md)
2. [B-federation-security-lab](labs/B-federation-security-lab/00-series-map.md)
3. [C-authorization-lab](labs/C-authorization-lab/00-series-map.md)
4. [D-data-api-lab](labs/D-data-api-lab/00-series-map.md)
5. [E-async-jobs-lab](labs/E-async-jobs-lab/00-series-map.md)
6. [F-realtime-lab](labs/F-realtime-lab/00-series-map.md)
7. [G-ops-lab](labs/G-ops-lab/00-series-map.md)
8. [workspace-backend](capstone/workspace-backend/00-series-map.md)

## 심화 트랙

1. [H-service-boundary-lab](labs/H-service-boundary-lab/00-series-map.md)
2. [I-event-integration-lab](labs/I-event-integration-lab/00-series-map.md)
3. [J-edge-gateway-lab](labs/J-edge-gateway-lab/00-series-map.md)
4. [K-distributed-ops-lab](labs/K-distributed-ops-lab/00-series-map.md)
5. [workspace-backend-v2-msa](capstone/workspace-backend-v2-msa/00-series-map.md)

## 읽는 방법

- 먼저 각 프로젝트의 `00-series-map.md`에서 문제, 구현 표면, 대표 검증 경로를 잡습니다.
- 그다음 `10-development-timeline.md`에서 실제 소스와 테스트가 어떤 순서로 읽히는지 따라갑니다.
- 단일 백엔드 기준선이 필요하면 필수 트랙을 먼저, 서비스 분해와 분산 복잡성이 필요하면 심화 트랙을 이어서 읽습니다.
