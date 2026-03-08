# Python 구현 안내

이 디렉터리는 `Selective Repeat`의 공개 구현을 담는다.

## 구성

- `src/selective_repeat.py`
- `tests/test_selective_repeat.py`

## 기준 명령

- 실행: `make -C study/Reliable-Transport/selective-repeat/problem run-solution`
- 검증: `make -C study/Reliable-Transport/selective-repeat/problem test`

## 구현 메모

- 상태: `verified`
- 현재 범위: 채널과 packet 포맷은 기존 RDT 과제와 같고, 차이는 sender/receiver 로직에 집중한다.
- 남은 약점: 실제 병렬 스레드 모델이 아님
- 남은 약점: sequence wraparound 미구현
- 남은 약점: 성능 실험 표 미작성
