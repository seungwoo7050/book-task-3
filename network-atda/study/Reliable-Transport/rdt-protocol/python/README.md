# Python 구현 안내

이 디렉터리는 `RDT Protocol`의 공개 구현을 담는다.

## 구성

- `src/gbn.py`
- `src/rdt3.py`
- `tests/test_rdt.py`

## 기준 명령

- 실행: `make -C study/Reliable-Transport/rdt-protocol/problem run-solution-rdt3`
- 검증: `make -C study/Reliable-Transport/rdt-protocol/problem test`

## 구현 메모

- 상태: `verified`
- 현재 범위: 현재 공개 구현은 rdt3.0과 GBN까지 다룬다. SR은 별도 프로젝트로 분리했다.
- 남은 약점: 실제 네트워크가 아닌 시뮬레이션 채널
- 남은 약점: GBN 성능 로그 자동 수집 미구현
- 남은 약점: 동시성 대신 단일 이벤트 루프 사용
