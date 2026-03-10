# Retrospective — 보안 강화 랩을 마치고 돌아보며

## 나아진 점

이 랩을 끝내고 가장 크게 달라진 건 **"인증 이후"의 지형도를 머릿속에 그릴 수 있게 된 것**이다. A랩에서 "비밀번호로 로그인하면 끝"이었다면, 이제는 "로그인 성공 → 외부 provider 연결 → 2FA 설정 → audit 기록"이라는 연속된 신뢰 강화 경로가 보인다.

federation과 2FA를 같이 묶은 설계가 결과적으로 좋았다. 따로 놓으면 "소셜 로그인"과 "이중 인증"이 별개 주제처럼 느껴지지만, 같은 랩에서 다루니 "둘 다 세션의 신뢰도를 높이는 메커니즘"이라는 공통점이 선명하게 드러났다.

audit logging을 같은 랩에 넣은 판단도 실무 감각을 높였다. 코드를 작성하면서 "이 지점에서 기록을 남겨야 나중에 추적이 가능하다"는 사고방식이 자연스럽게 습관이 된다.

## 여전히 약한 부분

솔직하게 말하면, 이 랩의 **Google integration은 아직 시뮬레이션**이다. 실제 OAuth2 연동에서는 authorization code를 access token으로 교환하고, id_token의 서명을 검증하는 과정이 있는데, 이 부분이 빠져 있다.

**TOTP의 보안 강도도 학습 친화적으로 단순화**했다. 실제 TOTP는 HMAC-SHA1 기반으로 시간 윈도우에 따라 코드가 바뀌지만, 이 랩에서는 UUID에서 추출한 고정 문자열을 사용한다.

**rate limiting은 아직 fully enforced behavior가 아니다.** 문서에서 "throttling이 필요하다"고 언급했지만, 실제로 N회 이상 실패한 IP를 차단하는 코드는 없다.

## 다시 살펴볼 것들

**단기**: Spring Security OAuth2 Client와 실제 provider config를 연결하는 실험. `spring-boot-starter-oauth2-client`는 이미 의존성에 포함되어 있으니, `application.yml`에 client registration만 추가하면 된다.

**중기**: Redis-backed rate limiter를 실제로 구현. sliding window counter 패턴으로 IP별 요청 빈도를 제한하고, 초과 시 429 응답을 반환하는 것까지.

**장기**: capstone과 연결해서 external identity persistence를 비교. provider subject를 PostgreSQL 테이블에 저장하고, 동일 이메일에 여러 provider가 연결된 경우를 처리하는 로직까지.

