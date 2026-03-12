# C-authorization-lab

인증과 별개로 membership, role, ownership 규칙을 어떻게 분리할지 정리하는 랩입니다.

- 상태: `verified scaffold`
- 실행 진입점: [spring/README.md](spring/README.md)

## 문제 요약

- "누구인가"를 확인하는 인증과 "무엇을 할 수 있는가"를 판단하는 인가는 다른 문제입니다.
- 초대, membership lifecycle, role 변경, ownership check를 service 단위에서 설명할 수 있어야 합니다.
- 상세 성공 기준과 제약은 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- organization 생성, invite 발급/수락, role 변경 endpoint를 갖는 authorization 랩을 만들었습니다.
- membership과 ownership 규칙을 service logic에 명시해 인가 판단이 어디서 일어나는지 보이게 했습니다.
- method security로 가기 전 단계의 baseline을 남겼습니다.

## 핵심 설계 선택

- 인증 랩과 섞지 않고 인가만 따로 떼어 규칙 자체를 읽기 쉽게 만들었습니다.
- policy engine이나 복잡한 외부 도구 대신 service logic으로 문제를 먼저 고정했습니다.
- persistence보다 membership 규칙 설명을 우선해 인메모리 state를 사용했습니다.

## 검증

```bash
cd spring
make lint
make test
make smoke
docker compose up --build
```

마지막 기록된 실제 검증 결과는 [../../docs/verification-report.md](../../docs/verification-report.md)에 있습니다.

## 이번 단계에서 일부러 남긴 것

- PostgreSQL 기반 membership persistence
- `@PreAuthorize` 중심 method security 재구성
- 외부 policy engine integration

## 다음에 읽을 문서

- canonical problem statement: [problem/README.md](problem/README.md)
- 실행과 검증: [spring/README.md](spring/README.md)
- 현재 구현 범위와 단순화: [docs/README.md](docs/README.md)
- 학습 로그와 재현 기록: [notion/README.md](notion/README.md)
