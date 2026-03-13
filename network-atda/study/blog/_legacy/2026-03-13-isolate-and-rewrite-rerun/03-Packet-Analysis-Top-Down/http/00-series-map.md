    # Series Map — HTTP Packet Analysis

    | 항목 | 내용 |
    | :--- | :--- |
    | 대상 프로젝트 | `03-Packet-Analysis-Top-Down/http` |
    | 문제 배경 | `Computer Networking: A Top-Down Approach`의 HTTP Wireshark 랩을 현재 저장소의 `problem/analysis/docs` 구조로 재정리한 프로젝트 |
    | 공개 답안 표면 | `analysis/src/http-analysis.md` |
    | 정식 검증 | `make -C study/03-Packet-Analysis-Top-Down/http/problem test` |
    | rewrite 방식 | `isolate-and-rewrite` |
    | legacy 보관 위치 | `_legacy/2026-03-13-isolate-and-rewrite/03-Packet-Analysis-Top-Down/http` |

    ## 프로젝트 경계
    - 이 프로젝트는 basic GET, conditional GET, 긴 문서 전송, embedded object 요청 체인을 packet evidence로 푸는 HTTP trace 읽기를 독립 문제로 다룬다.
    - `README.md`, `problem/`, `analysis/`, `docs/`가 한 폴더 아래에 닫혀 있어 다른 lab 없이도 범위 설명과 재검증이 가능하다.
    - canonical entrypoint는 `make -C study/03-Packet-Analysis-Top-Down/http/problem test`이며, 이번 재실행에서도 verify_answers.sh: `http` answer file passed content verification 신호를 확인했다.

    ## 이번 rewrite의 입력 표면
    - `problem/data/http-basic.pcapng`: 기본 GET 시나리오 trace
- `problem/data/http-conditional.pcapng`: conditional GET trace
- `problem/data/http-long-document.pcapng`: 긴 문서 전송 trace
- `problem/data/http-embedded-objects.pcapng`: 여러 객체가 포함된 페이지 trace
- `analysis/src/http-analysis.md`: 공개 답안
    - 소스 파일: `analysis/src/http-analysis.md`
    - 테스트는 `problem/script/*`와 canonical CLI를 중심으로 봤다.
    - `docs/concepts/conditional-get.md` - HTTP Conditional GET and Caching
- `docs/concepts/http-protocol.md` - HTTP/1.1 Protocol Reference
- `docs/concepts/http-versions.md` - HTTP 버전 비교: HTTP/1.0, HTTP/1.1, HTTP/2, HTTP/3
- `docs/concepts/wireshark-http.md` - Wireshark HTTP Analysis Techniques

    ## 이번 rewrite에서 제외한 입력
    - 기존 `study/blog/03-Packet-Analysis-Top-Down/http` 초안
    - `notion/`, `notion-archive/` 계열 노트
    - track 단위 회고나 다른 프로젝트 blog

    ## 이번 글에서 꼭 복원할 장면
    - Session 1: trace inventory와 CLI filter surface를 먼저 고정했다
- Session 2: answer file을 파트 순서대로 채웠다
- Session 3: docs와 verify script로 근거를 정리했다

    ## 이번 프로젝트가 남긴 학습 포인트
    - HTTP 상태 코드 해석
- `If-Modified-Since`와 `304 Not Modified`
- 긴 응답이 여러 TCP segment로 나뉘는 모습
- embedded object 요청 체인
