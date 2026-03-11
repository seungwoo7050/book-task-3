# B-federation-security-lab

로컬 인증 이후에 붙는 보안 강화 흐름을 따로 떼어 연습하는 랩입니다. 외부 로그인, 2단계 인증, 회복 코드, 감사 로그를 하나의 보안 랩으로 묶어 "계정 진입 경로를 어떻게 단단하게 만들 것인가"에 집중합니다.

## 문제 요약

- 이미 로컬 인증이 있는 서비스에 외부 로그인과 보안 강화 기능을 붙여야 한다고 가정합니다. 사용자는 Google 스타일 로그인으로 진입할 수 있어야 하고, 필요하면 2단계 인증과 recovery code를 사용할 수 있어야 합니다. 동시에 로그인 시도는 남용에 대비해 제한하고, 중요한 인증 이벤트는 기록해야 합니다.
- 외부 인증 공급자와 내부 사용자 계정의 연결 관계가 설명 가능해야 합니다.
- TOTP 등록과 검증 흐름이 독립된 단계로 구현되어야 합니다.
- 상세 성공 기준과 제외 범위는 [problem/README.md](problem/README.md)에 둡니다.

## 내 답

- Google 스타일 authorization-code 로그인
- provider-linked identity 관리
- TOTP 등록과 검증
- recovery code rotation
- 로그인 보안 이벤트 기록

## 핵심 설계 선택

- Google OIDC 로그인 흐름
- 외부 계정과 내부 사용자 계정 연결
- TOTP 기반 2단계 인증
- 테스트는 실제 Google 서비스가 아니라 mock 경로를 사용합니다.
- 제품 도메인 로직은 넣지 않고 인증 보안 흐름만 분리합니다.

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

- 실제 Google 서비스와의 end-to-end 통신 검증
- 제품 도메인별 권한과 리소스 모델
- 복수 공급자에 대한 공통 추상화 완성

## 다음 랩 또는 비교 대상

- 다음 단계는 [C-authorization-lab](../C-authorization-lab/README.md)입니다.
- 설계 설명은 [docs/README.md](docs/README.md), 학습 로그는 [notion/README.md](notion/README.md), 실행 진입점은 [fastapi/README.md](fastapi/README.md)에서 읽습니다.
