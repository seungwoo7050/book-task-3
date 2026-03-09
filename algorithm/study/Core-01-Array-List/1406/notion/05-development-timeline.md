# 개발 타임라인 — BOJ 1406 (에디터)

> 이 문서는 소스코드만으로는 추적할 수 없는 개발 과정을 순차적으로 기록한다.

## Phase 1: 프로젝트 초기화

```bash
python3 tools/migrate_legacy_to_study.py
```
legacy 경로 `legacy/core/01-array-list/silver-1406`에서 마이그레이션.

## Phase 2: 문제 분석
- 입력 크기 분석: 문자열 $\le 10^5$, 명령 $\le 5 \times 10^5$
- 리스트 insert 방식은 O(NM) → 시간 초과 예상
- Two-Stack 모델 채택 결정

## Phase 3: 솔루션 구현
- `python/src/solution.py` 작성
- `left = list(s)`: 초기 문자열을 left 스택에 넣음 (커서가 끝이므로)
- `right = []`: 커서 오른쪽은 비어 있음
- 4가지 명령에 대한 스택 연산 구현
- 최종 출력: `''.join(left) + ''.join(reversed(right))`

## Phase 4: 검증

```bash
cd study/Core-01-Array-List/1406/problem
make test
```
fixture 테스트 통과.

## Phase 5: 문서화
- docs/ 작성 (approach, edge-cases, 연결 리스트 개념)

## 사용한 도구

| 항목 | 상세 |
|------|------|
| OS | macOS (Darwin, ARM64) |
| Python | python3 |
| Shell | zsh |
| 빌드 도구 | GNU Make |
| 마이그레이션 | `tools/migrate_legacy_to_study.py` |
