# gateway

- 범위: public API 유지, cookie + CSRF, request id 전파, websocket fan-out
- 실행: `make install && make run`
- 테스트: `make test`
- 상태: 학습용 구현 완료
- 비고: 브라우저 쿠키는 gateway만 다루고 내부 서비스는 bearer claims만 받습니다.
