# Reliable Transport

checksum, sequence number, timer, sliding window가 어떻게 신뢰 전송을 만드는지 구현으로 확인하는 트랙이다.

## 왜 이 트랙인가

교재의 개념 흐름을 코드 상태 변수와 테스트 로그로 번역한다.

## 프로젝트 순서

1. [RDT Protocol](rdt-protocol/README.md) - `verified`
   핵심: rdt3.0과 Go-Back-N을 같은 채널 모델 위에서 비교하는 신뢰 전송 과제다.
2. [Selective Repeat](selective-repeat/README.md) - `verified`
   핵심: GBN의 한계를 보강하기 위해 추가한 선택 재전송 프로젝트다.

## 공통 규칙

- 코드 과제는 `problem/`과 `python/`을 분리한다.
- 패킷 분석 랩은 `problem/`과 `analysis/`를 분리한다.
- 시행착오와 회고는 `notion/`으로 밀어내고, 공개 README는 인덱스 역할만 맡긴다.
