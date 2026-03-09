# BOJ 2110 — 디버깅 기록

## 함정 1: 정렬 누락

**증상**: 판별 함수가 잘못된 결과 반환

**원인**: 집 좌표가 정렬되어 있지 않으면 탐욕적 판별이 성립하지 않음

**해결**: 입력 후 `houses.sort()` 필수

## 함정 2: 이진 탐색 범위

**증상**: 답이 0이나 음수로 나옴

**원인**: `lo = 0`으로 시작하면 `d = 0`이 feasible로 판정되어 의미 없는 답

**해결**: `lo = 1` (최소 거리는 1 이상)

## 함정 3: ans 갱신 시점

**증상**: feasible한 최대 d를 놓침

**원인**: 마지막 feasible한 mid를 기록하지 않음

**해결**: `if feasible(mid): ans = mid` 로 갱신하고, `lo = mid + 1`로 더 큰 값 탐색

## 확인 과정

```bash
make -C problem test
make -C problem run-cpp
```

Python과 C++ 결과 일치. PASS.
