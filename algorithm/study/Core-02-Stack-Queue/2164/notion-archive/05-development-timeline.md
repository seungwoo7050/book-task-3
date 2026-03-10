# 개발 타임라인 — BOJ 2164 (카드2)

## Phase 1: 프로젝트 초기화
```bash
python3 tools/migrate_legacy_to_study.py
```
legacy `legacy/core/02-stack-queue/silver-2164`에서 마이그레이션.

## Phase 2: 문제 분석
- 큐 패턴 인식: 앞에서 빼고 뒤에 넣기
- `collections.deque` 사용 결정

## Phase 3: 솔루션 구현
- `from collections import deque`
- `q = deque(range(1, n+1))` 초기화
- while 루프에서 popleft 2번 (버리기 + 뒤로 보내기)

## Phase 4: 검증
```bash
cd study/Core-02-Stack-Queue/2164/problem && make test
```
fixture 테스트 통과.

## 사용한 도구
| 항목 | 상세 |
|------|------|
| Python | python3, collections.deque |
| 빌드 도구 | GNU Make |
