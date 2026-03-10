# Debug Log — 보안 기능의 "이름"과 "실제 구현 깊이" 사이의 간극

## 마주한 문제

이 랩에서 겪은 가장 핵심적인 디버깅 포인트는 코드 버그가 아니라 **인식의 문제**였다.

"Google OAuth2", "TOTP", "throttling" 같은 단어가 문서에 들어가면, 저장소가 이 모든 것을 실제로 구현한 것처럼 읽히기 쉽다. 실제로는 Google integration은 mocked contract이고, TOTP 코드 생성은 단순화했으며, throttling은 문서화된 관심사 수준이다. blocking runtime defect는 없었지만, 문서가 구현 범위를 과장하면 독자가 이것을 reference implementation으로 오해한다.

## 근본 원인

보안 관련 용어는 그 자체로 무게감이 있다. simulated flow와 real integration을 문서에서 구분하지 않으면, 독자는 자연스럽게 "진짜 되는 거겠지"라고 가정한다.

## 어떻게 해결했는가

README와 notes에서 simplification을 명시했다. "Implemented now"와 "Important simplifications" 섹션을 분리하고, 각 기능의 현재 구현 수준을 명시적으로 기록했다.

```bash
make lint   # Spotless + Checkstyle 통과
make test   # Google callback, TOTP, audit 흐름 확인
```

## 남아 있는 기술 부채

- Redis-backed throttling enforcement가 아직 구현되지 않았다
- audit event가 인메모리 ArrayList에 저장되어 서버 재시작 시 사라진다
- real provider callback validation (authorization code → token 교환) 은 후속 과제다

