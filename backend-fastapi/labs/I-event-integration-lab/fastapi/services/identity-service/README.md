# identity-service

- 범위: 회원가입, 이메일 검증, 로컬 로그인, Google 스타일 로그인, refresh rotation
- 실행: `make install && make run`
- 테스트: `make test`
- 상태: 학습용 구현 완료
- 비고: 쿠키와 CSRF는 gateway가 처리하고, 이 서비스는 토큰 번들과 사용자 정보를 JSON으로 반환합니다.
