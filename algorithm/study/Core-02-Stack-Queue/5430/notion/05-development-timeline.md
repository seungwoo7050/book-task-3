# 개발 타임라인 — BOJ 5430 (AC)

## Phase 1: 프로젝트 초기화
```bash
python3 tools/migrate_legacy_to_study.py
```
legacy `legacy/core/02-stack-queue/gold-5430`에서 마이그레이션. C++ 비교 구현 유지.

## Phase 2: 문제 분석
- R의 O(n) 비용 인식 → 플래그 기반 해법 결정
- 입력 파싱 (JSON-like 배열) 분석
- `collections.deque` 사용 결정

## Phase 3: 솔루션 구현

### Python (`python/src/solution.py`)
- `is_reversed` 플래그로 R 처리
- D: 플래그에 따라 `dq.pop()` 또는 `dq.popleft()`
- 빈 배열 파싱을 `n == 0` 으로 분기
- 마지막에 `is_reversed`면 `dq.reverse()` 후 출력

### C++ (`cpp/src/solution.cpp`)
- 동일 로직을 deque<string>으로 구현

## Phase 4: 검증
```bash
cd study/Core-02-Stack-Queue/5430/problem && make test
```
fixture 테스트 통과. Python/C++ 교차 검증 완료.

## 사용한 도구
| 항목 | 상세 |
|------|------|
| Python | python3, collections.deque |
| C++ | g++-14, -std=c++17 |
| 빌드 도구 | GNU Make |
