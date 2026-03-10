# 검증 보고서

- 마지막 기록된 검증 실행일: `2026-03-09`
- 문서 갱신일: `2026-03-10`
- 문서 갱신 범위: README와 학습 노트 구조 정리
- 주의: `2026-03-10` 문서 개편에서는 아래 명령을 다시 실행하지 않았습니다. 이 문서는 `2026-03-09` 기준으로 실제 확인된 결과만 기록합니다.

## 당시 재실행한 기준 경로

- GitHub Actions 워크플로우: [.github/workflows/labs-fastapi.yml](../.github/workflows/labs-fastapi.yml)
- 대상: 일곱 개 lab + capstone의 모든 `fastapi/` 워크스페이스

## 당시 재실행한 명령

각 `fastapi/` 경로에서 아래 순서로 확인했고, Compose health probe는 저장소 루트에서 별도로 실행했습니다.

- 새 가상환경 생성
- `python3 -m compileall app tests`
- `make lint`
- `make test`
- `make smoke`
- `./tools/compose_probe.sh <workspace> <host-port>`에 해당하는 Compose health probe

## 마지막 기록된 결과 요약

- `labs/A-auth-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과
- `labs/B-federation-security-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과. PostgreSQL 데이터베이스 이름을 `DATABASE_URL`과 맞춘 뒤 재검증
- `labs/C-authorization-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과. 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화
- `labs/D-data-api-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과. 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화
- `labs/E-async-jobs-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과. 로컬 학습 실행을 위해 API 스키마 자동 초기화
- `labs/F-realtime-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과
- `labs/G-ops-lab/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과
- `capstone/workspace-backend/fastapi`: compile, lint, test, smoke, Compose live/ready probe 통과. 로컬 학습 실행을 위해 앱 시작 시 스키마 자동 초기화

## 이 보고서가 증명하는 것

- 문서에 적힌 Python 워크스페이스가 설치되고 실행됐다.
- 추적 중인 테스트 스위트가 당시 기준으로 통과했다.
- 로컬 Docker Compose 스택이 부팅되고 health endpoint에 응답했다.

## 이 보고서가 증명하지 않는 것

- AWS나 기타 클라우드에 실제 배포가 성공했다는 사실
- 장시간 부하, 성능, 복구 시나리오
- 테스트가 덮지 못한 보안 검토
- worker와 websocket client의 장시간 운영 안정성

학습 저장소의 검증 목표는 "제품 수준 보증"이 아니라 "다시 실행 가능하고 설명 가능한 상태"입니다.
