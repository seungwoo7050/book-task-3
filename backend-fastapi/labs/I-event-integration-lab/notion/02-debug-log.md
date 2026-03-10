# 디버그 로그

## 1. identity-service를 빼자 테스트용 JWT 생성 경로가 필요해졌다

- 증상: 이벤트 랩을 단독으로 돌릴 때 사용자 인증 흐름이 불필요하게 길어졌다.
- 판단: I 랩의 핵심은 인증이 아니라 outbox와 consumer 경계다.
- 수정: system test에서 JWT를 직접 만들고, `workspace-service`는 H 랩과 같은 claim 계약만 읽도록 유지했다.
- 검증: identity-service 없이도 workspace, invite, comment, relay, consume 흐름을 재현했다.

## 2. copied `workspace-service` 설정 누락이 다시 드러났다

- 증상: `access_token_ttl_seconds` 누락 때문에 service test가 실패했다.
- 원인: H/I/J/K로 구조를 복사하는 과정에서 설정 파일 차이가 생겼다.
- 수정: 모든 MSA 랩의 `workspace-service` 설정에 같은 필드를 복구했다.
- 검증: `services/workspace-service` 단위 테스트가 통과했다.

## 3. token `sub`가 UUID가 아니면 UUID column 처리에서 실패했다

- 증상: comment 흐름 이전에 workspace 생성 단계에서 UUID 변환 오류가 발생했다.
- 원인: 테스트용 claim의 `sub`를 사람이 읽기 쉬운 문자열로 넣었던 것이 문제였다.
- 수정: MSA 랩 공통으로 UUID 형식의 `sub`를 사용하도록 테스트를 수정했다.
- 검증: I 랩 system test에서 invite 수락, comment 작성, relay가 연속으로 동작했다.

## 4. Compose 실행에서는 `argon2-cffi` 누락이 숨어 있었다

- 증상: 로컬 서비스 테스트는 통과했지만 컨테이너 안에서는 `workspace-service`가 `argon2` import 에러로 죽었다.
- 원인: 루트 가상환경에 설치된 패키지가 로컬 테스트를 가려 주고 있었다.
- 수정: `workspace-service` 패키지 의존성에 `argon2-cffi`를 추가했다.
- 검증: I 랩 Compose 기반 system test와 smoke가 통과했다.
