# 04. Network Diagnostics and Routing blog

ICMP 기반 진단 도구와 distance-vector routing 구현으로 네트워크 계층 감각을 확장하는 단계입니다.

## 이 트랙에서 무엇을 따라가면 되나

이 레이어는 프로젝트를 나열하는 데서 멈추지 않고, 왜 이 순서가 자연스러운지까지 같이 보여 주려고 한다. 구현형 프로젝트는 진입점과 테스트를 먼저 보고, 분석형 프로젝트는 trace 질문과 filter target을 먼저 잡는 방식으로 읽으면 흐름이 편하다.

## 권장 읽기 순서

1. [ICMP Pinger](icmp-pinger/README.md) - ICMP echo request/reply를 raw socket 위에서 어디까지 직접 조립하고 해석했는가?
2. [Traceroute](traceroute/README.md) - UDP probe와 ICMP 응답을 엮어 hop 단위 경로를 어떻게 복원했는가?
3. [Distance-Vector Routing](routing/README.md) - distance-vector가 topology 입력에서 최종 routing table로 수렴하는 과정을 어떻게 보여 줬는가?

## 공통으로 보는 근거

- 프로젝트 README와 `problem/README.md`
- `problem/Makefile`의 실행/검증 target
- 구현형은 `python/` 또는 `cpp/`, 분석형은 `analysis/src/`
- 테스트 파일과 `docs/concepts/`
