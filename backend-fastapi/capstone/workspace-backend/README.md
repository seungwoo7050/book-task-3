# workspace-backend

이 프로젝트는 capstone v1 기준선입니다. 앞선 랩을 하나의 단일 FastAPI 백엔드로 다시 조합한 버전이며, 이후 `workspace-backend-v2-msa`와 비교할 때 기준이 되는 구조입니다.

이 capstone은 앞선 FastAPI 랩을 하나의 협업형 SaaS 백엔드로 다시 조합한 프로젝트입니다. 랩에서 따로 익힌 인증, 인가, 데이터 API, 비동기 작업, 실시간 전달을 한 구조 안에서 어떻게 통합하는지 보여 줍니다.

## 문제 요약

- 개별 랩으로 연습한 인증, 인가, 데이터 API, 비동기 알림, 실시간 전달을 하나의 협업형 SaaS 백엔드로 다시 조합합니다. 목표는 기능을 많이 붙이는 것이 아니라, 여러 경계를 함께 설명할 수 있는 통합 구조를 만드는 것입니다.
- 로컬 로그인과 외부 로그인 흐름이 같은 사용자 모델 안에서 설명 가능해야 합니다.
- 워크스페이스 멤버십과 역할이 프로젝트/태스크/댓글 API와 연결되어야 합니다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- 로컬 로그인과 Google 스타일 로그인
- 워크스페이스 멤버십과 초대
- 프로젝트, 태스크, 댓글 API
- 알림 큐와 실시간 전달
- health endpoint

## 핵심 설계 선택

- 인증과 인가를 제품형 워크스페이스 도메인에 묶는 방법
- 프로젝트, 태스크, 댓글을 중심으로 한 협업 API 구조
- queued notification과 realtime delivery의 결합
- 랩 코드를 공용 패키지로 묶지 않고 다시 구현합니다.
- 프런트엔드, 정적 자산, 실제 클라우드 인프라는 제외합니다.

## 검증

```bash
make lint
make test
make smoke
docker compose up --build
```

- 실행과 환경 설명은 [fastapi/README.md](fastapi/README.md)에서 다룹니다.
- 마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 제외 범위

- 프런트엔드 렌더링과 정적 자산 제공
- 실제 클라우드 배포 자동화
- 랩 코드를 공용 패키지로 묶는 리팩터링

## 다음 랩 또는 비교 대상

- 비교 대상은 [workspace-backend-v2-msa](../workspace-backend-v2-msa/README.md)입니다.
- 심화 트랙으로 넘어가려면 [H-service-boundary-lab](../../labs/H-service-boundary-lab/README.md)부터 다시 분해 과정을 읽습니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.
