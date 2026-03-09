# 개발 타임라인 — BOJ 10828 (스택)

## Phase 1: 프로젝트 초기화
```bash
python3 tools/migrate_legacy_to_study.py
```
legacy 경로 `legacy/core/02-stack-queue/bronze-10828`에서 마이그레이션.

## Phase 2: 문제 분석
- 5가지 스택 명령 구현
- Python list를 스택으로 직접 사용 결정

## Phase 3: 솔루션 구현
- `python/src/solution.py` 작성
- 명령 파싱: `input().split()` 후 분기
- 출력 모아두기: `out` 리스트에 결과 수집, `'\n'.join(out)`으로 출력

## Phase 4: 검증
```bash
cd study/Core-02-Stack-Queue/10828/problem && make test
```
fixture 테스트 통과.

## 사용한 도구
| 항목 | 상세 |
|------|------|
| Python | python3 |
| 빌드 도구 | GNU Make |
| 마이그레이션 | `tools/migrate_legacy_to_study.py` |
