# SMTP Client Blog

이 디렉터리는 `01-Application-Protocols-and-Sockets/smtp-client` 프로젝트를 `isolate-and-rewrite` 방식으로 다시 쓴 source-first blog 레이어다. 기존 초안은 `_legacy/2026-03-13-isolate-and-rewrite/01-Application-Protocols-and-Sockets/smtp-client`로 옮겼고, 이번 rewrite에서는 기존 blog 내용을 입력 근거로 쓰지 않았다.

## 이번 rewrite에서 사용한 근거
- 프로젝트 README와 `problem/README.md`
- `problem/Makefile`과 실제 재실행한 canonical CLI
- 소스 표면: `python/src/smtp_client.py`
- 테스트/검증 표면: `python/tests/test_smtp_client.py`
- 반복 개념 표면: `docs/concepts/email-format.md`, `docs/concepts/smtp-errors.md`, `docs/concepts/smtp.md`

## 파일 구성
- `00-series-map.md` - 문제 범위, 공개 표면, legacy 격리 경로를 고정한다.
- `01-evidence-ledger.md` - Session 단위로 근거와 CLI, 코드 앵커를 정리한다.
- `02-structure.md` - 최종 글을 어떤 순서와 장면으로 풀지 설계한다.
- `10-development-timeline.md` - 최종 chronological blog 본문.

## canonical verification
- `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`
- 현재 재실행 신호: SMTP Client Test Suite: 전체 SMTP dialogue 완료, 성공 메시지와 대화 로그 확인, 총 3 passed
