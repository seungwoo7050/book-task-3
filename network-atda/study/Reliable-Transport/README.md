# Reliable Transport

checksum, sequence number, timer, sliding window가 어떻게 신뢰 전송을 만드는지 코드로 확인하는 트랙입니다.

## 이 트랙이 맡는 역할

패킷 손실과 손상이 있는 채널 위에서 송신자와 수신자가 어떤 상태를 기억해야 하는지 직접 구현하게 만듭니다. 이론식이 코드 상태 변수로 바뀌는 과정을 보기 좋습니다.

## 추천 선수 지식

- 기본적인 자료구조와 상태 기계 개념
- TCP의 ACK와 재전송 아이디어를 아주 대략적으로 알고 있으면 도움이 됩니다.
- Python으로 간단한 시뮬레이터를 읽고 수정할 수 있으면 충분합니다.

## 권장 프로젝트 순서

1. [RDT Protocol](rdt-protocol/README.md) - `verified`
   rdt3.0과 Go-Back-N을 같은 채널 모델 위에서 비교합니다.
2. [Selective Repeat](selective-repeat/README.md) - `verified`
   개별 ACK와 수신 버퍼를 갖는 Selective Repeat를 구현해 GBN과 대비합니다.

## 공통 읽기 방법

- `problem/README.md`에서 프로토콜 규칙과 성공 기준을 읽습니다.
- `python/README.md`에서 구현 파일과 검증 명령을 확인합니다.
- `docs/README.md`에서 이론 비교 문서를 다시 읽습니다.
- `notion/README.md`는 구현 선택과 디버깅 흔적을 보존한 공개 백업용 노트입니다.

## 포트폴리오로 확장하기

- Go-Back-N과 Selective Repeat의 차이를 표나 시퀀스 다이어그램으로 정리하면 학습 깊이가 잘 드러납니다.
- 단순히 테스트 통과를 보여 주기보다 손실/손상 시나리오에서 어떤 상태 전이가 일어나는지 설명하세요.
- 성능 비교 그래프나 재전송 횟수 요약을 추가하면 구현 프로젝트가 분석 프로젝트로 확장됩니다.
