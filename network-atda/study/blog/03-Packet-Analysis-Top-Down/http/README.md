# HTTP Packet Analysis Blog

이 문서 묶음은 `http` 랩을 "HTTP가 어떻게 생겼는가"보다 "짧은 trace 네 개를 이어 붙이면 browser request pattern을 어디까지 복원할 수 있는가"라는 질문으로 다시 읽는다. 현재 공개 답안은 기본 GET, conditional GET, long document, embedded objects trace를 각각 따로 읽고, `200 -> 304`, `single object -> 7 TCP data segments`, `serial image fetch` 같은 패턴을 frame 번호로 고정한다. 따라서 이 lab의 핵심은 HTTP 문법 소개보다 request/response가 transport 위에서 어떻게 드러나는지를 trace별로 비교하는 데 있다.

이번 재작성은 기존 blog 본문이 아니라 다음 근거만 사용했다.

- 문제 정의: `study/03-Packet-Analysis-Top-Down/http/problem/README.md`
- 답안 경계: `README.md`, `analysis/README.md`, `analysis/src/http-analysis.md`
- 실제 검증: 2026-03-14 재실행한 `make -C network-atda/study/03-Packet-Analysis-Top-Down/http/problem test`
- 보조 필터: `make -C .../http/problem filter-basic`, `filter-conditional`, `filter-embedded`

## 읽는 순서

1. [`00-series-map.md`](./00-series-map.md)
2. [`10-development-timeline.md`](./10-development-timeline.md)
3. [`01-evidence-ledger.md`](./01-evidence-ledger.md)
4. [`02-structure.md`](./02-structure.md)

## 이번에 다시 확인한 검증 상태

- 정식 검증 명령: `make -C network-atda/study/03-Packet-Analysis-Top-Down/http/problem test`
- 결과: `PASS: http answer file passed content verification`
- 보조 필터에서 재확인한 값:
  - basic trace: `GET /kurose_ross_small/HTTP/index.html`, response `200`, `Content-Length 36`
  - conditional trace: 두 번째 GET에 `If-Modified-Since`, response `304 Not Modified`
  - embedded trace: `index.html -> img1.png -> img2.png` 순서의 직렬 GET

## 지금 남기는 한계

- trace는 모두 `HTTP/1.1`이며 `HTTP/2` 이상은 범위 밖이다.
- browser별 헤더 차이나 connection pooling 정책은 이 자료만으로 일반화할 수 없다.
- long document trace는 segment 수는 보이지만 장기 cwnd 진화까지 보여 주지는 않는다.
