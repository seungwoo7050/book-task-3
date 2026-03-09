# 개발 타임라인 — BOJ 10807 (개수 세기)

> 이 문서는 소스코드만으로는 추적할 수 없는 개발 과정을 순차적으로 기록한다.

## Phase 1: 프로젝트 초기화

```bash
python3 tools/migrate_legacy_to_study.py
```

legacy 경로 `legacy/core/01-array-list/bronze-10807`에서 마이그레이션.

## Phase 2: 문제 분석 및 fixture 준비
- BOJ 10807 문제 페이지에서 입출력 형식 확인
- `problem/data/`에 fixture 배치

## Phase 3: 솔루션 구현
- `python/src/solution.py` 작성
- `sys.stdin.readline` 입력 패턴
- `arr.count(v)`로 빈도 계산, `print()`로 출력

## Phase 4: 검증

```bash
cd study/Core-01-Array-List/10807/problem
make test
```
fixture 테스트 통과.

## Phase 5: 문서화
- docs/ 작성 (approach, edge-cases, reproducibility)

## 사용한 도구

| 항목 | 상세 |
|------|------|
| OS | macOS (Darwin, ARM64) |
| Python | python3 |
| Shell | zsh |
| 빌드 도구 | GNU Make |
| 마이그레이션 | `tools/migrate_legacy_to_study.py` |
