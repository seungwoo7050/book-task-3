# Debug Log — scaffold를 "검증 가능한 상태"로 유지하기

## 마주한 문제

이 랩에서 겪은 가장 핵심적인 문제는 전통적인 의미의 버그가 아니었다. 오히려 **"scaffold의 문서가 구현 범위를 과장하지 않도록 유지하는 것"** 자체가 가장 큰 도전이었다.

처음에 README를 작성할 때, 자연스럽게 "register, login, refresh, logout, verification, reset" 같은 기능 이름을 나열하게 된다. 문제는 이 중 일부(verification, reset)가 아직 API shape 수준에서만 존재하고, 실제 동작하는 코드가 없다는 것이었다.

증상을 구체적으로 말하면, auth persistence와 mail lifecycle이 아직 얕기 때문에 README가 구현 범위를 과장하면 금방 모순이 생겼다. 처음에는 "scaffold니까 기능 이름만 있으면 충분히 설명될 것"이라고 생각했지만, 이건 **신뢰 문제**다. 기술 문서에서 한 번 "여기 적힌 게 실제로 안 된다"를 경험하면, 독자는 나머지 내용도 의심하기 시작한다.

확인해보니 README와 docs가 현재 상태를 `verified scaffold`로 명시하고 next improvements를 분리하는 구조가 필요했다.

## 근본 원인

이 랩은 완성품이 아니라 **구조 학습용 scaffold**다. 그런데 문서가 완성품처럼 기능을 나열하면, 구현된 것과 모델 수준인 것의 경계가 사라진다.

구체적으로, `AuthDemoService`는 register, login, refresh, logout, me 다섯 가지만 실제로 구현한다. verification token은 `RegisterResult` record에 포함되지만, 그 토큰을 실제로 검증하는 엔드포인트는 없다. password reset도 마찬가지다. 이 차이가 문서에 반영되지 않으면, 독자가 코드를 읽을 때 혼란이 생긴다.

## 어떻게 해결했는가

접근 방식은 단순하지만 효과적이었다. **모든 문서에서 "구현된 것"과 "아직 모델 수준인 것"을 명시적으로 분리**했다.

`docs/README.md`에 "Implemented now" 섹션과 "Important simplifications" 섹션을 나누었고, `spring/README.md`에도 "Known gaps"를 별도로 명시했다. 이렇게 하면 독자가 문서를 읽자마자 "아, 이 부분은 아직 안 되는구나"를 즉시 파악할 수 있다.

검증은 세 단계로 확인했다:

```bash
make lint    # Spotless + Checkstyle 코드 스타일 검사 통과
make test    # AuthFlowApiTest — register→login→refresh 흐름과 CSRF 거절 테스트 통과
make smoke   # LabInfoApiSmokeTest — 앱 부팅과 /api/v1/lab/info 응답 확인
```

## 남아 있는 기술 부채

- **persisted verification/reset flow**: `RegisterResult`에 `verificationToken`이 포함되지만 이를 받아 처리하는 엔드포인트가 없다. 실제 사용자 활성화 흐름을 구현하려면 DB 저장과 토큰 만료 로직이 필요하다.
- **response cookie assertion**: 현재 테스트는 JSON body에서 토큰을 꺼내 쓴다. 프로덕션에서는 `Set-Cookie` 헤더의 `HttpOnly`, `Secure`, `SameSite` 속성을 검증하는 테스트가 추가되어야 한다.

