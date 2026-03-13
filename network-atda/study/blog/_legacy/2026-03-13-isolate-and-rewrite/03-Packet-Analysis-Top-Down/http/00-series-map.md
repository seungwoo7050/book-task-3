# HTTP Packet Analysis 시리즈 지도

## 이 프로젝트를 한 줄로

HTTP를 "텍스트 프로토콜"로만 외우지 않고, GET 한 줄과 응답 한 줄이 TCP 위에서 어떻게 증거로 남는지 네 개의 trace로 좁혀 가는 기록이다.

## 시작 전에 고정한 자료

- 제공 trace: `problem/data/http-basic.pcapng`, `http-conditional.pcapng`, `http-long-document.pcapng`, `http-embedded-objects.pcapng`
- 실행 진입점: `problem/Makefile`
- 사용자 답안: `study/03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`
- 보조 개념 문서: `docs/concepts/wireshark-http.md`

## 이 시리즈에서 따라갈 질문

1. 기본 GET/응답 한 쌍만으로도 HTTP 버전, 상태 코드, `Content-Length`, `Connection`까지 어디서 확정할 수 있는가.
2. `If-Modified-Since`가 붙은 두 번째 요청은 첫 번째 요청과 무엇이 다르고, 왜 응답 본문이 사라지는가.
3. 긴 문서 trace에서 `Content-Length: 9000`이라는 숫자를 TCP data segment 개수와 어떻게 연결해야 하는가.
4. embedded object trace에서 이미지 요청이 직렬인지 병렬인지 어떤 frame 순서로 판단하는가.

## 검증 명령

- 기본 시나리오: `make -C study/03-Packet-Analysis-Top-Down/http/problem filter-basic`
- 조건부 요청: `make -C study/03-Packet-Analysis-Top-Down/http/problem filter-conditional`
- 긴 문서 전송: `make -C study/03-Packet-Analysis-Top-Down/http/problem filter-long`
- embedded object: `make -C study/03-Packet-Analysis-Top-Down/http/problem filter-embedded`
- 답안 검증: `make -C study/03-Packet-Analysis-Top-Down/http/problem test`

## 글 구성

| 파일 | 역할 |
| :--- | :--- |
| `00-series-map.md` | 어떤 trace를 어떤 순서로 읽을지 먼저 고정한다. |
| `10-development-timeline.md` | 기본 GET → conditional GET → 긴 문서 → embedded object 순서로 evidence를 쌓아 간다. |
