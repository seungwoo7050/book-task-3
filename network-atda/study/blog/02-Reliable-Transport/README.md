# 02. Reliable Transport blog

손실과 손상이 있는 채널에서 송신자와 수신자가 어떤 상태를 기억해야 하는지 시뮬레이션으로 확인하는 단계입니다.

## 이 트랙에서 무엇을 따라가면 되나

이 레이어는 프로젝트를 나열하는 데서 멈추지 않고, 왜 이 순서가 자연스러운지까지 같이 보여 주려고 한다. 구현형 프로젝트는 진입점과 테스트를 먼저 보고, 분석형 프로젝트는 trace 질문과 filter target을 먼저 잡는 방식으로 읽으면 흐름이 편하다.

## 권장 읽기 순서

1. [RDT Protocol](rdt-protocol/README.md) - rdt3.0과 Go-Back-N의 핵심 차이를 같은 채널 모델 위에서 어떻게 드러냈는가?
2. [Selective Repeat](selective-repeat/README.md) - 개별 ACK과 수신 버퍼링이 Go-Back-N 다음 단계에서 어떤 차이를 만드는가?

## 공통으로 보는 근거

- 프로젝트 README와 `problem/README.md`
- `problem/Makefile`의 실행/검증 target
- 구현형은 `python/` 또는 `cpp/`, 분석형은 `analysis/src/`
- 테스트 파일과 `docs/concepts/`
