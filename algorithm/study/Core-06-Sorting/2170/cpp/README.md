# C++ 비교 구현 안내

## 이 폴더의 역할

이 폴더는 Python 기준 풀이를 다른 언어로 비교해 볼 때 쓰는 보조 구현을 담는다. 프로젝트의 canonical 설명은 여전히 Python 쪽을 먼저 읽는다.

## 먼저 볼 파일

- `src/solution.cpp`

## 기준 명령

- 실행: `make -C study/Core-06-Sorting/2170/problem run-cpp`
- 검증: `make -C study/Core-06-Sorting/2170/problem test`

## 현재 범위

- 비교 답안: `구간을 시작점 기준 정렬 후 병합해 총 길이 계산`

## 남은 약점

- README와 `docs/`의 설명 기준선은 Python 구현 쪽에 둔다.
- 언어별 미세 최적화 비교는 최소한만 남기고, 핵심 판단 근거만 확인한다.
