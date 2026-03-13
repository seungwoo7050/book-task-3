# Proxy Lab Structure Outline

이 문서는 최종 blog를 어떤 곡선으로 읽히게 만들지 미리 고정하는 편집 설계 메모다. 근거는 모두 `01-evidence-ledger.md`와 실제 소스에서 왔고, 여기서는 그 근거를 어떤 순서로 보여 줄 때 가장 자연스럽게 이해되는지에 집중한다.

## 이 시리즈의 편집 원칙

Proxy Lab에서는 결론을 먼저 선언하기보다, 구현이 어디서부터 단단해졌는지를 보여 주는 편이 더 중요하다. 그래서 최종 글은 문제를 좁히는 첫 장면, 설계가 갈라지는 중간 장면, 검증이 닫히는 마지막 장면의 세 구간으로 나눈다. 각 구간은 코드와 CLI가 함께 등장해야 하고, 다음 phase로 넘어가는 질문이 문단 끝에 남아 있어야 한다.

## 최종 글의 흐름

1. 도입에서 `make clean && make test`와 현재 재작성 범위를 먼저 밝히고, 독자가 이 글이 어떤 evidence layer 위에 서 있는지 알게 한다.
2. 본문은 Phase 1 URI 파싱과 upstream request 조립을 먼저 세운다 -> Phase 2 동시성 처리와 LRU cache를 serve path에 붙인다 -> Phase 3 origin server 기반 end-to-end test로 닫는다 순서로 간다. 순서를 바꾸지 않는 이유는 이 흐름이 README와 테스트가 실제로 요구하는 구현 순서에 가장 가깝기 때문이다.
3. 마지막에는 CLI excerpt와 남은 질문을 붙여, 이 프로젝트가 어디까지 닫혔고 어디가 다음 학습 포인트인지 분명하게 남긴다.

## 1. Phase 1 - URI 파싱과 upstream request 조립을 먼저 세운다

이 구간의 중심 장면은 프록시의 첫 번째 일은 캐시가 아니라 올바른 요청을 origin으로 다시 보내는 일이다.

본문에서는 먼저 header 정규화 전에 `parse_uri`와 `build_request`가 흔들리면 네트워크 디버깅이 전부 흐려질 거라고 봤다. 그 다음 문단에서는 URI 파싱, header append helper, canonical request builder를 먼저 묶어 upstream surface를 고정했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `parse_uri`, `build_request`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: request builder가 먼저 고정돼 있어 이후 캐시/동시성 문제를 분리해서 볼 수 있다.
- 장면이 끝날 때 남길 문장: concurrent serve와 cache path로 넘어간다.

## 2. Phase 2 - 동시성 처리와 LRU cache를 serve path에 붙인다

이 구간의 중심 장면은 `handle_client`, `cache_lookup`, `cache_store`, `promote_entry`가 실제 프록시의 중간 설계 축이다.

본문에서는 먼저 멀티클라이언트 처리를 붙이는 순간 캐시 일관성과 request forwarding이 함께 흔들릴 거라고 예상했다. 그 다음 문단에서는 client handler에서 forwarding과 caching을 한 번에 다루되, cache list 조작은 helper로 분리해 LRU 이동을 명확히 했다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `handle_client`, `cache_lookup`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: cache helper 분리가 있어야 동시성과 캐시 논의를 같은 파일 안에서도 추적할 수 있다.
- 장면이 끝날 때 남길 문장: self-owned origin server로 전체 루프를 검증한다.

## 3. Phase 3 - origin server 기반 end-to-end test로 닫는다

이 구간의 중심 장면은 proxy는 unit-level helper만으로 끝나지 않고 실제 요청/응답 루프를 확인해야 한다.

본문에서는 먼저 공식 driver 없이도 `tests/origin_server.py`와 shell harness가 있으면 구현 흐름을 충분히 재현할 수 있다고 판단했다. 그 다음 문단에서는 README와 Makefile을 `run_proxy_tests.sh` 중심으로 묶어 end-to-end 검증을 공개 표면에 올렸다. 이 두 문장을 나란히 두어, 독자가 '처음엔 무엇을 믿었고 그 믿음이 어떤 코드 때문에 바뀌었는가'를 따라가게 만든다.

- 반드시 보여 줄 코드: `Handler`, `$ORIGIN_PID`
- 붙일 CLI: `make clean && make test`
- 강조할 검증 신호: origin fixture와 shell harness가 마지막 검증 신호를 남긴다.
- 장면이 끝날 때 남길 문장: request surface, concurrent handler, cache verification 순서로 닫는다.

## Fixed CLI Anchor

```bash
(cd /Users/woopinbell/work/book-task-3/cs-core/study/Systems-Programming/proxylab/c && make clean && make test)
```

이 명령은 최종 글 마지막에서 README 계약이 여전히 살아 있다는 사실을 다시 확인하는 closing shot로 사용한다.
