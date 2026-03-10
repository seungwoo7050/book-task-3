# workspace-service

- 범위: 워크스페이스, 초대, 프로젝트, 태스크, 댓글, outbox relay
- 실행: `make install && make run`
- 테스트: `make test`
- 상태: 학습용 구현 완료
- 비고: 사용자 식별은 bearer claims만 사용하고, `identity-service` DB를 직접 읽지 않습니다.
