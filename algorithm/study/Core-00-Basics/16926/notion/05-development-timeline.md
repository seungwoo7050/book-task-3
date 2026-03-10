# 개발 타임라인

> 프로젝트: 배열 돌리기 1
> 이 문서는 학습자가 현재 저장소 기준으로 구현과 검증 과정을 끝까지 다시 밟아 볼 수 있게 정리한 재현 문서다.

## 왜 이 문서가 중요한가

- `docs/references/reproducibility.md`는 빠른 실행 명령을 확인하는 문서이고, 여기서는 그 명령을 어떤 순서와 맥락에서 실행했는지까지 남긴다.
- 학습 레포에서 재현성은 '명령 하나를 안다'가 아니라 '어떤 문서를 읽고 어떤 확인을 거쳐 현재 구현에 도달하는지 따라갈 수 있다'는 뜻에 더 가깝다.

## 재현 시작점

- 현재 기준 경로: `study/Core-00-Basics/16926`
- 먼저 확인할 빠른 명령: `make -C problem test`
- 함께 읽을 빠른 문서: `../docs/references/reproducibility.md`, `01-approach-log.md`, `02-debug-log.md`

## 단계별 기록

아래 메모는 `notion-archive/05-development-timeline.md`의 실제 기록을 현재 공개 노트 기준으로 다듬고, 지금 다시 따라 할 때 필요한 설명을 덧붙인 버전이다.

### 단계 1: 프로젝트 초기화

#### 마이그레이션
provenance 메모: 이전 마이그레이션 기록상 원본 경로는 `legacy/core/00-basics/silver-16926`였다. 현재 읽을 기준 경로는 `study/Core-00-Basics/16926`이다.

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

### 단계 2: 문제 분석

#### 문제 원문 확인
핵심 제약 파악:
- $N, M \le 300$ → 배열 크기는 관리 가능
- $R \le 10^9$ → 모듈러 최적화 필수
- $\min(N,M)$이 짝수 → 레이어 분해가 깔끔하게 떨어짐

#### 알고리즘 설계
1. 레이어 개수: `min(N, M) // 2`
2. 각 레이어를 1차원 ring으로 추출
3. `R % len(ring)` 만큼 shift
4. ring을 배열에 다시 써넣기

#### 테스트 fixture
- 4×4 배열, R=2 → 출력 확인
- 4×4 배열, R=1 → 단일 회전 확인

### 단계 3: 솔루션 구현

#### Python 구현 (`python/src/solution.py`)
- `sys.stdin.readline` 입력 패턴
- 레이어별 4방향 순회로 ring 추출 (윗변→오른변→아랫변→왼변)
- `ring[r:] + ring[:r]` 슬라이싱으로 반시계 회전
- 같은 4방향 순서로 ring을 배열에 재기입
- `' '.join(map(str, row))`로 행 단위 출력

#### 구현 시 주의점
- 코너 중복 방지를 위한 범위 조정 (각 변의 시작/끝 인덱스 설정)
- ring 길이가 레이어마다 다르므로 모듈러를 레이어별로 계산

### 단계 4: 검증

#### fixture 테스트
```bash
cd study/Core-00-Basics/16926/problem
make test
```
결과: `Results: 2/2 passed, 0 failed`

#### 수동 검증
```bash
python3 ../python/src/solution.py <<'EOF'
3 4 1
1 2 3 4
5 6 7 8
9 10 11 12
EOF
```
3×4 직사각형에서 레이어 하나만 존재하는 경우의 회전 확인.

### 단계 5: 문서화

#### docs/ 작성
- `concepts/layer-decomposition.md`: 레이어 분해 개념 설명
- `concepts/edge-cases.md`: 최소 크기, 큰 R, 직사각형 등
- `references/approach.md`: 접근 전략과 정당성
- `references/reproducibility.md`: 실행 환경과 관측 결과

#### Cross-Track 메모
README에 "Core-05-Simulation을 시작할 때 다시 복습한다"고 기록.

### 사용한 도구 및 환경

| 항목 | 상세 |
|------|------|
| OS | macOS (Darwin, ARM64) |
| Python | python3 |
| Shell | zsh |
| 빌드 도구 | GNU Make |
| provenance | 이전 마이그레이션 기록 참고 |
| 버전 관리 | Git |
