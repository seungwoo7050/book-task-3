# 지식 인덱스

## 재사용 가능한 개념

- 외부 로그인은 "외부에서 인증됨"과 "내부 사용자로 연결됨" 두 단계로 봐야 한다.
- 2FA가 필요한 사용자는 최종 세션 전의 중간 상태를 가져야 한다.
- 보안 랩일수록 로직보다 먼저 설정 정합성을 확인해야 한다.

## 용어집

- `OIDC`: OAuth 2.0 위에서 사용자 identity 정보를 다루는 표준
- `pending auth`: 최종 세션이 발급되기 전, 추가 검증이 남은 상태
- `recovery code`: TOTP를 사용할 수 없을 때를 대비한 1회성 백업 코드

## 참고 자료

- 제목: `labs/B-federation-security-lab/problem/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: 새 문제 프레이밍에 보안 범위를 맞추기 위해 확인했다.
  - 배운 점: 이 랩의 핵심은 provider 연동 자체보다 identity linking과 multi-step auth flow다.
  - 반영 결과: 새 `00-problem-framing.md`와 `01-approach-log.md`에 반영했다.
- 제목: `labs/B-federation-security-lab/fastapi/README.md`
  - 확인 날짜: `2026-03-10`
  - 참고 이유: 실제 실행 경로와 Alembic 선행 적용 여부를 현재 워크스페이스 기준으로 다시 확인하기 위해 읽었다.
  - 배운 점: 이 랩의 실행 경로는 인증 보안 흐름만큼이나 마이그레이션 선행 적용이 중요하다.
  - 반영 결과: 새 `02-debug-log.md`와 `05-development-timeline.md`에 실행 순서를 더 명확히 적었다.
