# Retrospective

## "로그인"을 분해하고 나서 보인 것들

A-auth-lab에서의 로그인은 하나의 동작이었다. 이메일과 비밀번호를 보내면 끝. 이 랩에서 로그인은 최소 세 단계로 분해된다: (1) Google에서 authorization code 받기, (2) code를 토큰으로 교환하고 identity를 내부 시스템에 매핑하기, (3) 2FA가 있으면 추가 검증 거치기. 각 단계가 실패할 수 있고, 각 단계에 고유한 보안 관심사가 있다.

이 분해가 학습으로 남긴 가장 큰 것은 **상태 전이의 명시성**이다. `callback` 응답이 `"status": "authenticated"` 또는 `"status": "requires_2fa"`를 반환하고, 후자의 경우 `pending_auth_token`이라는 별도 토큰 유형이 존재한다는 것. 이 중간 상태를 명시적 토큰으로 표현하는 설계는 "인증 중"이라는 애매한 상태를 코드에서 타입으로 구분할 수 있게 만든다.

## External Identity 설계의 가치

`external_identities` 테이블을 User와 분리한 것은 처음에는 과한 설계처럼 보였다. Google 하나만 쓰는데 왜 별도 테이블이 필요할까? 하지만 이 분리 덕분에 "같은 이메일이지만 다른 provider"라는 시나리오의 설계가 자연스러워진다. User 테이블은 내부 identity(handle, email, display_name)만 관리하고, provider별 정보(provider_subject, profile JSON)는 external_identities에 남는다. 나중에 GitHub나 Apple 로그인을 추가해도 User 스키마를 바꿀 필요가 없다.

## 아직 약한 것들

**Live provider 검증 부재**: mock이 커버하는 것은 "우리 코드가 올바른 순서로 올바른 메서드를 호출하는가"까지다. Google이 실제로 반환할 수 있는 edge case(이메일 미인증, consent 거부, 토큰 만료 직전 응답)는 테스트되지 않는다.

**Recovery code의 보관 정책**: recovery code를 8개 생성하고 해시로 저장하는 것까지는 구현했지만, 남은 개수를 사용자에게 표시하거나, 마지막 코드 사용 시 경고하는 UX 흐름은 없다. 서버 로직만으로는 "recovery code를 잃어버렸을 때 어떻게 되는가?"에 답하기 어렵다.

**Auth와 Authorization의 단절**: 이 랩은 "이 사람이 누구인가"만 다룬다. "이 사람이 무엇을 할 수 있는가"는 C-authorization-lab의 영역이다. 두 랩을 별도로 만든 것은 학습 분리를 위한 의도적 선택이지만, 현실에서는 인증과 권한이 같은 요청 파이프라인에서 작동한다.

## 다시 보고 싶은 것들

- Redis를 활용한 throttling의 정밀한 윈도우 제어와 분산 환경에서의 동작
- refresh token reuse 감지 시 사용자에게 알림을 보내는 정책
- A-auth-lab의 로컬 인증과 이 federation 인증을 하나의 서비스에서 동시에 지원하는 통합 설계
