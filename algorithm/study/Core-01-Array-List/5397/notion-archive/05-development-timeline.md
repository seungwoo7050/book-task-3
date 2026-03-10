# 개발 타임라인 — BOJ 5397 (키로거)

> 이 문서는 소스코드만으로는 추적할 수 없는 개발 과정을 순차적으로 기록한다.

## Phase 1: 프로젝트 초기화

```bash
python3 tools/migrate_legacy_to_study.py
```
legacy 경로 `legacy/core/01-array-list/gold-5397`에서 마이그레이션.
C++ 비교 구현도 함께 유지.

## Phase 2: 문제 분석
- 1406과 동일한 Two-Stack 패턴 인식
- 차이점: 다중 테스트 케이스, 총 입력 길이 $\le 5 \times 10^6$
- 출력 최적화 필요성 판단 (`sys.stdout.write`)

## Phase 3: 솔루션 구현

### Python (`python/src/solution.py`)
- 각 테스트 케이스마다 left/right 스택 초기화
- 키 입력 문자열을 한 글자씩 순회
- `sys.stdout.write()`로 출력

### C++ (`cpp/src/solution.cpp`)
- 동일한 Two-Stack 로직
- C++ 빌드: `g++-14 -std=c++17 -O2 -Wall`

## Phase 4: 검증

```bash
cd study/Core-01-Array-List/5397/problem
make test
```
fixture 테스트 통과. Python/C++ 교차 검증 완료.

## Phase 5: 문서화
- docs/ 작성
- 1406과의 연결 관계 명시

## 사용한 도구

| 항목 | 상세 |
|------|------|
| OS | macOS (Darwin, ARM64) |
| Python | python3 |
| C++ | g++-14, -std=c++17 |
| Shell | zsh |
| 빌드 도구 | GNU Make |
| 마이그레이션 | `tools/migrate_legacy_to_study.py` |
