# HTTP Packet Analysis Evidence Ledger

## 이번에 읽은 자료

- 문제 사양: `study/03-Packet-Analysis-Top-Down/http/problem/README.md`
- 답안 엔트리: `study/03-Packet-Analysis-Top-Down/http/analysis/src/http-analysis.md`
- 검증 스크립트: `study/03-Packet-Analysis-Top-Down/http/problem/script/verify_answers.sh`
- 실행 표면: `study/03-Packet-Analysis-Top-Down/http/problem/Makefile`

## 핵심 근거

- `filter-basic` 출력:
  - frame `4` GET `/kurose_ross_small/HTTP/index.html`
  - frame `6` response `200`, `Content-Length 36`
- `filter-conditional` 출력:
  - 첫 GET에는 conditional header 없음
  - 둘째 GET에는 `If-Modified-Since: Mon, 17 Feb 2025 06:59:02 GMT`
  - 응답은 `304 Not Modified`
- `http-analysis.md` long document section:
  - GET 1개
  - server data frames `#5-#11`
  - `Content-Length 9000`
- `filter-embedded` 출력:
  - frame `4` `/index.html`
  - frame `7` `/img1.png` referer `/index.html`
  - frame `10` `/img2.png` referer `/index.html`

## 테스트 근거

`make -C network-atda/study/03-Packet-Analysis-Top-Down/http/problem test`

결과:

- `PASS: http answer file passed content verification`

## 이번에 고정한 해석

- 이 lab는 "HTTP header field를 나열하는 문제"가 아니라 trace 종류에 따라 관찰 포인트가 어떻게 달라지는지 배우는 문제다.
- conditional GET의 핵심은 `If-Modified-Since` 헤더 자체보다, body가 사라진 `304` response로 교환 비용이 줄어드는 장면이다.
- embedded object trace는 referer와 요청 순서만으로도 병렬 여부를 꽤 강하게 판정할 수 있다.
