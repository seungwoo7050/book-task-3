# HTTP Packet Analysis — Development Timeline

HTTP Packet Analysis는 구현 코드를 쓰는 프로젝트가 아니라 trace를 읽는 절차를 복원하는 프로젝트였다. 그래서 이번 rewrite는 Wireshark 화면 기억이 아니라 `problem/Makefile`의 filter target, `analysis/src/http-analysis.md`의 part ordering, 그리고 `make -C study/03-Packet-Analysis-Top-Down/http/problem test` 재실행 신호를 묶는 방식으로 진행했다.

```bash
make -C study/03-Packet-Analysis-Top-Down/http/problem filter-basic
make -C study/03-Packet-Analysis-Top-Down/http/problem filter-conditional
make -C study/03-Packet-Analysis-Top-Down/http/problem filter-long
make -C study/03-Packet-Analysis-Top-Down/http/problem filter-embedded
make -C study/03-Packet-Analysis-Top-Down/http/problem test
```

## Session 1 — trace inventory와 CLI filter surface를 먼저 고정했다
먼저 확인한 가설은 "analysis 프로젝트도 구현 프로젝트처럼 먼저 entrypoint를 잡지 않으면 chronology가 흐려진다"였다. 그래서 `problem/Makefile`, `analysis/src/http-analysis.md`를 기준으로 trace를 잘랐고, 실제 조치는 `make -C study/03-Packet-Analysis-Top-Down/http/problem filter-basic` 같은 filter target을 기준으로 trace를 나누고, answer file의 파트 구조를 `Part 1: Basic HTTP GET / Response`, `Part 2: Conditional GET` 순으로 고정했다.
결과적으로 `make -C study/03-Packet-Analysis-Top-Down/http/problem filter-basic`를 다시 호출했을 때 어떤 질문이 어떤 trace와 filter에 기대는지 다시 찾아갈 수 있는 표면을 확인했다. 이 장면이 중요한 이유는 `analysis/src/http-analysis.md`를 packet evidence와 함께 묶어 둘 수 있기 때문이다.

## Session 2 — answer file을 파트 순서대로 채웠다
먼저 확인한 가설은 "가장 눈에 띄는 frame만 적으면 설명이 편해 보이지만, part 순서대로 답을 채워야 문제 범위가 유지된다"였다. 그래서 `analysis/src/http-analysis.md`의 `Part 1: Basic HTTP GET / Response` / `Part 2: Conditional GET` / Part 3: Long Documents, Part 4: Embedded Objects를 기준으로 trace를 잘랐고, 실제 조치는 먼저 `Part 1: Basic HTTP GET / Response`와 `Part 2: Conditional GET`를 채우고, 이어서 `Part 3: Long Documents, Part 4: Embedded Objects` 구간까지 답을 확장했다. 필요할 때는 `make -C study/03-Packet-Analysis-Top-Down/http/problem filter-conditional` 같은 filter를 다시 호출해 frame evidence를 좁혔다.
결과적으로 `make -C study/03-Packet-Analysis-Top-Down/http/problem filter-conditional`를 다시 호출했을 때 analysis/src 답안이 문제의 part ordering과 같은 순서로 닫히기 시작한 상태를 확인했다. 이 장면이 중요한 이유는 `If-Modified-Since`와 `304 Not Modified`를 packet evidence와 함께 묶어 둘 수 있기 때문이다.

## Session 3 — docs와 verify script로 근거를 정리했다
먼저 확인한 가설은 "analysis 글도 마지막에 `무엇을 봤는가`뿐 아니라 `어떤 개념으로 읽었는가`를 남겨야 다음 trace로 이어진다"였다. 그래서 `problem/script/verify_answers.sh`를 기준으로 trace를 잘랐고, 실제 조치는 개념 문서 제목과 trace evidence를 맞춰 보고, verify script를 다시 돌려 answer file completeness를 확인했다.
결과적으로 `make -C study/03-Packet-Analysis-Top-Down/http/problem test`를 다시 호출했을 때 verify_answers.sh: `http` answer file passed content verification를 확인했다. 이 장면이 중요한 이유는 HTTP 상태 코드 해석과 `If-Modified-Since`와 `304 Not Modified`를 packet evidence와 함께 묶어 둘 수 있기 때문이다.

## Verification and Boundaries
마지막에는 `make -C study/03-Packet-Analysis-Top-Down/http/problem test`를 다시 돌려 verify_answers.sh: `http` answer file passed content verification를 확인했다. 고정 trace 기반이라는 한계는 그대로 남기고, 아래 범위 밖의 해석은 의도적으로 확장하지 않았다.
- `HTTP/2` 이상은 다루지 않습니다.
- 브라우저별 헤더 차이는 관찰 범위 밖입니다.
- 실시간 캡처 대신 고정 trace에 기반합니다.
