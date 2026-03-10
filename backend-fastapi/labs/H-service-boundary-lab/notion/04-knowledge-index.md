# 지식 인덱스

## 먼저 적용할 판단 규칙

- 서비스 분리에서 첫 질문은 라우터가 아니라 데이터 ownership이다.
- 토큰 claim으로 충분한 정보를 전달할 수 있다면 다른 서비스 DB를 읽지 않는 쪽이 더 건강하다.
- shared ORM 모델이 편해 보이기 시작하면 경계가 약해지고 있다는 신호로 본다.

## 핵심 개념과 사용 조건

### `DB ownership`

언제 쓰는가:
- 각 서비스가 자기 데이터에 대해서만 직접 읽기/쓰기를 하도록 강제하고 싶을 때
- 서비스 경계를 단순 폴더 분리가 아니라 운영 책임 분리로 설명하고 싶을 때

실패 징후:
- `workspace-service`가 사용자 상세를 얻으려고 `identity-service` DB를 직접 보고 싶어진다.
- 테이블 설계보다 공용 모델 재사용이 먼저 눈에 들어온다.

이 랩의 근거:
- [../fastapi/services/identity-service/app/db/models/auth.py](../fastapi/services/identity-service/app/db/models/auth.py)
- [../fastapi/services/workspace-service/app/db/models/platform.py](../fastapi/services/workspace-service/app/db/models/platform.py)

### `bearer claims`

언제 쓰는가:
- 원격 사용자 정보를 최소 계약으로만 넘기고 싶을 때
- 사용자 식별과 도메인 membership 판단을 분리하고 싶을 때

주의할 점:
- claim이 너무 얇으면 서비스가 다시 원격 DB 조회를 하고 싶어진다.
- claim이 너무 두꺼우면 토큰이 profile cache처럼 변질된다.

이 랩의 근거:
- [../fastapi/services/identity-service/app/api/v1/routes/auth.py](../fastapi/services/identity-service/app/api/v1/routes/auth.py)
- [../fastapi/services/workspace-service/app/domain/services/platform.py](../fastapi/services/workspace-service/app/domain/services/platform.py)

### `cross-DB lookup 금지`

왜 중요한가:
- 지금 당장은 편해도, ownership 설명과 장애 격리 설명이 함께 무너진다.
- H 랩의 목적은 “토큰 하나로 workspace 생성까지 간다”를 증명하는 것이지, 서비스 사이의 은밀한 DB join을 허용하는 것이 아니다.

이 랩의 근거:
- [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)

## 이 랩에서 빨리 확인할 포인트

1. [../fastapi/tests/test_system.py](../fastapi/tests/test_system.py)에서 identity 토큰으로 workspace를 생성하는 흐름을 본다.
2. [../fastapi/services/workspace-service/app/domain/services/platform.py](../fastapi/services/workspace-service/app/domain/services/platform.py)에서 `claims["sub"]`, `claims["email"]`만으로 owner/membership을 처리하는 방식을 본다.
3. [../fastapi/services/workspace-service/app/db/models/platform.py](../fastapi/services/workspace-service/app/db/models/platform.py)에서 workspace 쪽 DB가 identity 모델을 직접 들고 있지 않은 점을 확인한다.

## 실패 징후와 먼저 의심할 것

| 징후 | 먼저 의심할 것 | 이유 |
| --- | --- | --- |
| workspace 생성 전에 identity DB를 다시 조회하고 싶다 | claim 계약이 너무 얇다 | 서비스 경계보다 조회 편의가 앞선다 |
| 테스트 토큰의 `sub`가 UUID 형식과 안 맞는다 | DB ownership + claim contract | 모델과 토큰 계약이 서로 다른 식별자를 가정하고 있다 |
| shared model을 import하고 싶다 | 경계 붕괴 | 서비스 분리를 폴더 분리 수준으로만 보고 있다 |

## 참고 자료

- 제목: `labs/A-auth-lab/problem/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: access token의 최소 계약을 다시 정리하기 위해 확인했다.
  - 배운 점: 인증 랩의 토큰 구조를 서비스 경계 계약으로 재사용할 수 있다.
  - 반영 결과: H 랩의 성공 기준과 debug log에 반영했다.
- 제목: `labs/C-authorization-lab/problem/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: claim 기반 권한 판단이 어디까지 가능한지 다시 보기 위해 읽었다.
  - 배운 점: 인가 규칙은 토큰 claim과 도메인 membership을 구분해야 설명이 쉬워진다.
  - 반영 결과: H 랩 docs와 notion의 경계 설명에 반영했다.
- 제목: `labs/H-service-boundary-lab/fastapi/tests/test_system.py`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: 실제 검증이 어떤 계약을 증명하는지 기록하기 위해 확인했다.
  - 배운 점: “identity 토큰으로 workspace 생성” 한 문장으로 이 랩의 핵심을 설명할 수 있다.
  - 반영 결과: `05-development-timeline.md`와 verification 메모에 반영했다.
