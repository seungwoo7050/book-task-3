# Knowledge Index — 이 랩에서 가져갈 개념들

## 재사용 가능한 핵심 개념

### External Identity Linking

외부 identity provider(Google, GitHub 등)가 발급한 **provider subject(고유 식별자)**를 내부 user identity에 연결하는 설계 패턴이다. 이 랩의 `FederationSecurityDemoService.callback()`이 이 동작을 보여준다 — `email`과 `subject`를 받아 `linkedIdentities`에 매핑한다.

이 패턴이 중요한 이유는 같은 사용자가 여러 provider로 로그인할 수 있기 때문이다. "Google로 가입한 사용자"와 "이메일로 가입한 사용자"가 같은 사람이라면, 두 identity를 하나의 내부 user에 연결해야 한다. capstone에서 이 구조가 PostgreSQL 테이블로 확장될 때 다시 등장한다.

### Second Factor (2FA)

primary auth(비밀번호 또는 OAuth) 성공 이후에 **별도의 증명을 추가하는 보강 단계**다. 비밀번호가 유출되더라도 2FA가 남아 있으면 계정 탈취를 막을 수 있다.

이 랩에서는 TOTP(Time-based One-Time Password) 방식을 모델링했다. `setupTotp()`가 secret과 recovery code를 발급하고, `verifyTotp()`가 코드를 검증한다. 실제 TOTP는 HMAC-SHA1 기반이지만, 이 scaffold에서는 UUID 파생 문자열로 단순화했다.

### Audit Log

민감한 인증 이벤트를 **사후 설명 가능하게 기록하는 관행**이다. "누가 언제 로그인했는지", "2FA 검증이 실패했는지", "비정상적인 패턴이 있는지"를 추적하는 기반이 된다.

이 랩의 `FederationSecurityDemoService`에서 모든 주요 메서드가 `auditEvents.add()`를 호출하는 구조가 이 관행을 반영한다. 현재는 인메모리 ArrayList이지만, 프로덕션에서는 별도 audit 테이블이나 로그 시스템(ELK, CloudWatch 등)으로 보내야 한다.

## 용어 정리

### Provider Subject

외부 identity provider가 사용자에게 부여한 **고유 식별자**다. Google의 경우 `sub` 클레임으로 전달되며, 동일 Google 계정에 대해 항상 같은 값이 반환된다. 이메일과 달리 변경되지 않으므로, identity linking의 키로 사용하기에 적합하다.

### TOTP (Time-based One-Time Password)

시간 기반 일회용 코드 생성 방식이다. 서버와 클라이언트가 같은 secret을 공유하고, 현재 시간을 기반으로 6자리 코드를 생성한다. 30초마다 코드가 바뀌므로, 코드를 탈취해도 짧은 시간 내에만 유효하다. Google Authenticator, Authy 같은 앱이 이 방식을 사용한다.

## 참고 자료

- **B-federation-security-lab docs README** (`docs/README.md`): simplification과 next improvements를 맞추기 위해 확인했다. real provider integration과 Redis throttling이 아직 후속 개선 대상이라는 점을 확인하고, 문제 정의에서 mocked contract라는 전제를 고정했다.
- **RFC 6238 (TOTP)**: TOTP 알고리즘의 표준 명세. 이 랩에서는 표준의 보안 강도까지 구현하지 않았지만, 흐름(setup → verify)의 구조를 이해하는 데 참고했다.

