    # Series Map — SMTP Client

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `01-Application-Protocols-and-Sockets/smtp-client` |
    | 문제 배경 | `Computer Networking: A Top-Down Approach`의 SMTP 메일 클라이언트 과제를 현재 저장소 구조에 맞게 정리한 프로젝트 |
    | 공개 답안 표면 | `python/src/smtp_client.py` |
    | 정식 검증 | `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/01-Application-Protocols-and-Sockets/smtp-client` |

    ## 프로젝트 경계
    - 이 프로젝트는 220/250/354/221 reply code를 확인하며 DATA 종료 마커까지 직접 보내는 SMTP 대화를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `python/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/01-Application-Protocols-and-Sockets/smtp-client/problem test`이며, 이번 재실행에서도 SMTP Client Test Suite: 전체 SMTP dialogue 완료, 성공 메시지와 대화 로그 확인, 총 3 passed 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/code/smtp_client_skeleton.py`: 시작용 skeleton 코드
- `problem/script/mock_smtp_server.py`: 로컬 모의 SMTP 서버
- `problem/script/test_smtp.sh`: 정식 검증 스크립트
    - 소스 파일: `python/src/smtp_client.py`
    - 테스트 파일: `python/tests/test_smtp_client.py`
    - `docs/concepts/email-format.md` - Email Message Format
- `docs/concepts/smtp-errors.md` - SMTP 응답 코드와 에러 처리 패턴
- `docs/concepts/smtp.md` - SMTP Protocol Reference

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/01-Application-Protocols-and-Sockets/smtp-client` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: 실행 entrypoint와 최소 runtime surface를 먼저 고정했다
- Session 2: 핵심 protocol/algorithm branch를 채웠다
- Session 3: canonical test와 문서로 경계를 닫았다

    ## 이번 프로젝트가 남긴 학습 포인트
    - 3자리 SMTP 응답 코드에 따른 제어 흐름
- `CRLF`와 `DATA` 종료 구분자 처리
- envelope 주소와 헤더 주소의 차이
- 예상하지 못한 응답 코드를 빠르게 중단시키는 fail-fast 구조
