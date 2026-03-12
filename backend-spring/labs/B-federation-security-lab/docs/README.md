# B-federation-security-lab 설계 메모

이 문서는 인증 강화 랩의 현재 구현 범위와 의도적 한계를 요약한다.

## 현재 구현 범위

- Google authorize URL 생성과 callback-shaped linking flow
- TOTP setup/verify 예시 흐름
- in-memory audit event 기록

## 의도적 단순화

- Google integration은 contract modeling 수준이다
- TOTP 코드는 학습 가독성을 위해 단순화했다
- throttling은 문제 인식 위주이며 hard enforcement는 아직 아니다

## 다음 개선 후보

- Spring Security OAuth2 client와 실제 provider config 연결
- provider subject와 audit event의 PostgreSQL persistence
- Redis-backed rate limiter
