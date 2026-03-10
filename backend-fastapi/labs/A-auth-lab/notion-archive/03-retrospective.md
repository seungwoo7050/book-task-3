# Retrospective

## 분리해서 비로소 보인 것들

이 랩을 마치고 나서 가장 또렷하게 느낀 것은, **로컬 auth를 OAuth와 분리해 두니 보안 경계를 설명하기가 훨씬 쉬워졌다**는 점이다.

처음에는 "어차피 다음 랩에서 OAuth를 추가하니까, 미리 같이 넣으면 효율적이지 않겠냐"고 생각했다. 하지만 실제로 분리해 보니, 로컬 credential lifecycle의 각 단계가—signup, email verification, login, token rotation, logout—독립적으로 명확하게 보였다. OAuth까지 같이 넣었다면 "Google provider에서 뭐가 안 되는 건지 vs 우리 토큰 로직이 잘못된 건지" 원인 분리가 어려웠을 것이다.

cookie + CSRF pairing을 별도 학습 주제로 다룬 것도 좋은 판단이었다. 브라우저 환경에서 HttpOnly cookie로 세션을 유지하면서 동시에 CSRF 공격을 막아야 한다는 문제는, 말로 들으면 간단해 보이지만 실제로 구현하면 "어떤 cookie에 httponly를 켜고 어떤 것에 끄느냐, SameSite는 lax로 하느냐 strict로 하느냐" 같은 구체적인 결정이 계속 나온다. 이런 결정들을 다른 주제 없이 집중해서 내릴 수 있었던 게 이 랩의 강점이었다.

Mailpit을 포함한 로컬 개발 경험도 "학습 저장소다운 단순함"을 만들어냈다. 실제 메일이 날아갈 필요 없이, Mailpit UI에서 검증 토큰이 담긴 메일을 확인할 수 있으니, 이메일 검증 흐름 자체에 집중할 수 있었다.

## 여전히 약한 지점들

솔직하게 말하면, 몇 가지는 아직 충분하지 않다.

**테스트가 SQLite 중심이다.** PostgreSQL에서만 나타나는 동작 차이—트랜잭션 격리 수준, timestamp precision, constraint enforcement 순서 같은 것들—을 아직 완전히 커버하지 못한다. `conftest.py`에서 in-memory SQLite를 쓰는 건 속도 면에서 탁월하지만, 운영 환경의 진짜 동작을 100% 대변하지는 않는다.

**이메일 검증과 재설정은 백엔드 흐름 중심이다.** 실제 사용자가 브라우저에서 이메일 링크를 클릭하는 UX와는 거리가 있다. API 테스트에서 토큰을 직접 꺼내서 검증하는 방식이니, 프론트엔드 관점의 경험은 별도로 보충해야 한다.

**브라우저 환경에서의 cookie 동작은 API 테스트만으로는 충분히 설명되지 않는다.** `TestClient`는 cookie를 잘 다루지만, 실제 브라우저의 SameSite 정책, cross-origin 요청에서의 cookie 전파 같은 것들은 API 수준에서는 검증이 안 된다.

## 다음에 다시 볼 것들

- reset token과 verification token의 만료/재사용 규칙을 더 엄격하게 분리할 수 있다. 현재는 둘 다 비슷한 패턴으로 처리하고 있지만, 실무에서는 구분해야 할 지점이 더 있을 수 있다.
- PostgreSQL 기반 integration 테스트 커버리지를 늘려야 한다. Compose 환경에서 실제 PostgreSQL에 연결하는 테스트를 추가하면 SQLite와의 갭을 줄일 수 있다.
- 같은 주제를 Spring Security 트랙과 비교하는 메모를 추가하면, 프레임워크 간 인증 설계 차이를 시각화할 수 있다.
