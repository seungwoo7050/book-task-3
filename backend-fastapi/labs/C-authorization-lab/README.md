# C-authorization-lab

인증이 끝난 뒤 "누가 무엇을 할 수 있는가"를 분리해서 다루는 랩입니다. 워크스페이스, 초대, 역할, 소유권을 중심으로 인가 규칙을 서비스 계층에서 어떻게 설명할지 연습합니다.

## 문제 요약

- 워크스페이스 기반 협업 서비스에서 "누가 무엇을 할 수 있는가"를 명확히 해야 합니다. 초대, 역할 변경, 소유권, 읽기/쓰기 가능 범위를 코드로 표현하고, 인증 자체와는 분리해서 설명 가능한 구조를 만들어야 합니다.
- 워크스페이스 생성과 초대 흐름이 분리된 규칙으로 정리되어야 합니다.
- 역할별로 가능한 작업이 문서와 코드에서 일관되게 드러나야 합니다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- 워크스페이스 생성
- 초대 발행과 응답
- 역할 변경
- 문서/리소스 접근 제어

## 핵심 설계 선택

- workspace membership 모델
- invitation 생성, 수락, 거절 흐름
- RBAC 역할 경계
- 인증은 별도 헤더 기반 actor 모델로 단순화합니다.
- 핵심은 "누가 할 수 있나"이지 "어떻게 로그인했나"가 아닙니다.

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

- 실제 로그인 시스템과 세션 관리
- 정책 엔진 같은 고급 외부 권한 시스템
- 조직 간 멀티테넌시 전체 설계

## 다음 랩 또는 비교 대상

- 다음 단계는 [D-data-api-lab](../D-data-api-lab/README.md)입니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.
