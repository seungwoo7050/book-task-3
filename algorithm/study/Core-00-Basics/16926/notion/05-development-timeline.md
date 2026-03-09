# 개발 타임라인 — BOJ 16926 (배열 돌리기 1)

> 이 문서는 소스코드만으로는 추적할 수 없는 개발 과정을 순차적으로 기록한다.

## Phase 1: 프로젝트 초기화

### 마이그레이션
legacy 구조(`legacy/core/00-basics/silver-16926`)에서 마이그레이션 도구를 통해 변환했다.

```bash
python3 tools/migrate_legacy_to_study.py
```

생성된 구조:
```
study/Core-00-Basics/16926/
├── README.md
├── problem/
│   ├── Makefile
│   ├── code/        # starter.py, starter.cpp
│   ├── data/        # 2세트의 input/output fixture
│   └── script/      # test.sh
├── python/
│   └── src/         # solution.py
├── docs/
│   ├── concepts/    # layer-decomposition.md, edge-cases.md
│   └── references/  # approach.md, overview.md, reproducibility.md
└── notion/
```

## Phase 2: 문제 분석

### 문제 원문 확인
핵심 제약 파악:
- $N, M \le 300$ → 배열 크기는 관리 가능
- $R \le 10^9$ → 모듈러 최적화 필수
- $\min(N,M)$이 짝수 → 레이어 분해가 깔끔하게 떨어짐

### 알고리즘 설계
1. 레이어 개수: `min(N, M) // 2`
2. 각 레이어를 1차원 ring으로 추출
3. `R % len(ring)` 만큼 shift
4. ring을 배열에 다시 써넣기

### 테스트 fixture
- 4×4 배열, R=2 → 출력 확인
- 4×4 배열, R=1 → 단일 회전 확인

## Phase 3: 솔루션 구현

### Python 구현 (`python/src/solution.py`)
- `sys.stdin.readline` 입력 패턴
- 레이어별 4방향 순회로 ring 추출 (윗변→오른변→아랫변→왼변)
- `ring[r:] + ring[:r]` 슬라이싱으로 반시계 회전
- 같은 4방향 순서로 ring을 배열에 재기입
- `' '.join(map(str, row))`로 행 단위 출력

### 구현 시 주의점
- 코너 중복 방지를 위한 범위 조정 (각 변의 시작/끝 인덱스 설정)
- ring 길이가 레이어마다 다르므로 모듈러를 레이어별로 계산

## Phase 4: 검증

### fixture 테스트
```bash
cd study/Core-00-Basics/16926/problem
make test
```
결과: `Results: 2/2 passed, 0 failed`

### 수동 검증
```bash
python3 ../python/src/solution.py <<'EOF'
3 4 1
1 2 3 4
5 6 7 8
9 10 11 12
EOF
```
3×4 직사각형에서 레이어 하나만 존재하는 경우의 회전 확인.

## Phase 5: 문서화

### docs/ 작성
- `concepts/layer-decomposition.md`: 레이어 분해 개념 설명
- `concepts/edge-cases.md`: 최소 크기, 큰 R, 직사각형 등
- `references/approach.md`: 접근 전략과 정당성
- `references/reproducibility.md`: 실행 환경과 관측 결과

### Cross-Track 메모
README에 "Core-05-Simulation을 시작할 때 다시 복습한다"고 기록.

## 사용한 도구 및 환경

| 항목 | 상세 |
|------|------|
| OS | macOS (Darwin, ARM64) |
| Python | python3 |
| Shell | zsh |
| 빌드 도구 | GNU Make |
| 마이그레이션 | `tools/migrate_legacy_to_study.py` |
| 버전 관리 | Git |
