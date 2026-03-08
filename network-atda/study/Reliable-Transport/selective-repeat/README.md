# Selective Repeat

| 항목 | 내용 |
| :--- | :--- |
| 상태 | `verified` |
| 레거시 원본 | `legacy/Programming-Assignments/rdt-protocol + 신규 보강 프로젝트` |
| 정식 검증 | `make -C study/Reliable-Transport/selective-repeat/problem test` |

## 한 줄 요약

GBN의 한계를 보강하기 위해 추가한 선택 재전송 프로젝트다.

## 문제 요약

기존 packet/channel helper를 재사용해, 개별 ACK와 수신 버퍼를 사용하는 Selective Repeat를 구현한다.

## 이 프로젝트를 여기 둔 이유

레거시 문서가 직접 암시했지만 비어 있던 bridge project를 채워 Reliable Transport 트랙을 완성한다.

## 제공 자료

- `problem/code/channel.py`와 `packet.py` 재사용
- `problem/code/selective_repeat_skeleton.py` 신규 skeleton
- `problem/script/test_selective_repeat.sh` 신규 검증

## 학습 포인트

- 개별 packet timer
- receiver buffer와 in-order delivery
- ACKed set과 sender base 업데이트
- GBN과 SR trade-off 비교

## 실행과 검증

- 실행: `make -C study/Reliable-Transport/selective-repeat/problem run-solution`
- 검증: `make -C study/Reliable-Transport/selective-repeat/problem test`
- 구현 위치: `python/src/`
- 보조 테스트: `python/tests/`

## 현재 범위와 한계

채널과 packet 포맷은 기존 RDT 과제와 같고, 차이는 sender/receiver 로직에 집중한다.

- 현재 한계: 실제 병렬 스레드 모델이 아님
- 현재 한계: sequence wraparound 미구현
- 현재 한계: 성능 실험 표 미작성

## Public / Private 경계

- `problem/`은 제공 자료와 canonical 검증 래퍼만 둔다.
- `python/` 또는 `analysis/`는 공개 구현과 공개 답안만 둔다.
- `docs/`는 반복해서 참고할 개념 메모만 유지한다.
- `notion/`은 노션 업로드용 작업 노트이며 저장소 공개 구조에 의존하지 않는다.
