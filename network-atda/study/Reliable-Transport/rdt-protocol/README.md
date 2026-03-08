# RDT Protocol

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Programming-Assignments/rdt-protocol` |
| 정식 검증 | `make -C study/Reliable-Transport/rdt-protocol/problem test` |

## 한 줄 요약

rdt3.0과 Go-Back-N을 같은 채널 모델 위에서 비교하는 신뢰 전송 과제다.

## 문제 요약

손실과 손상이 있는 채널에서 checksum, sequence number, timer, ACK를 이용해 메시지를 정확히 전달하는 두 프로토콜을 구현한다.

## 이 프로젝트를 여기 둔 이유

전송 계층 메커니즘을 가장 직접적으로 체험하는 중심 과제로, 이후 Selective Repeat 추가의 기준점 역할을 한다.

## 제공 자료

- `problem/code/channel.py` 비신뢰 채널
- `problem/code/packet.py` packet helper
- `problem/data/test_messages.txt` 테스트 데이터
- `problem/script/test_rdt.sh` 통합 검증

## 학습 포인트

- alternating bit와 cumulative ACK 차이
- timeout 기반 재전송
- sliding window 기본 구조
- 이벤트 루프만으로 프로토콜 시뮬레이션하는 방법

## 실행과 검증

- 실행: `make -C study/Reliable-Transport/rdt-protocol/problem run-solution-rdt3`
- 검증: `make -C study/Reliable-Transport/rdt-protocol/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 현재 범위와 한계

현재 공개 구현은 rdt3.0과 GBN까지 다룬다. SR은 별도 프로젝트로 분리했다.

- 현재 한계: 실제 네트워크가 아닌 시뮬레이션 채널
- 현재 한계: GBN 성능 로그 자동 수집 미구현
- 현재 한계: 동시성 대신 단일 이벤트 루프 사용

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
