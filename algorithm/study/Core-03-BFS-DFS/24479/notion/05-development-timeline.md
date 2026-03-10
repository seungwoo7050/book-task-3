# 개발 타임라인

> 프로젝트: 알고리즘 수업 - 깊이 우선 탐색 1
> 이 문서는 학습자가 현재 저장소 기준으로 구현과 검증 과정을 끝까지 다시 밟아 볼 수 있게 정리한 재현 문서다.

## 왜 이 문서가 중요한가

- `docs/references/reproducibility.md`는 빠른 실행 명령을 확인하는 문서이고, 여기서는 그 명령을 어떤 순서와 맥락에서 실행했는지까지 남긴다.
- 학습 레포에서 재현성은 '명령 하나를 안다'가 아니라 '어떤 문서를 읽고 어떤 확인을 거쳐 현재 구현에 도달하는지 따라갈 수 있다'는 뜻에 더 가깝다.

## 재현 시작점

- 현재 기준 경로: `study/Core-03-BFS-DFS/24479`
- 먼저 확인할 빠른 명령: `make -C problem test`
- 함께 읽을 빠른 문서: `../docs/references/reproducibility.md`, `01-approach-log.md`, `02-debug-log.md`

## 단계별 기록

아래 메모는 `notion-archive/05-development-timeline.md`의 실제 기록을 현재 공개 노트 기준으로 다듬고, 지금 다시 따라 할 때 필요한 설명을 덧붙인 버전이다.

### 단계 1: 프로젝트 구조 생성

생성된 구조: `problem/`, `python/`, `docs/`, `notion/`

### 단계 2: 1260 코드 기반 수정

```bash
# 1260 풀이를 참고하여 변형
cp ../1260/python/src/solution.py python/src/solution.py
vi python/src/solution.py
```

변경 사항:
1. BFS 부분 제거 (DFS만 필요)
2. `dfs_order` 리스트 대신 `result` 배열 + `order` 카운터
3. `setrecursionlimit` 200000으로 상향
4. 출력을 `'\n'.join`으로 변경

### 단계 3: 테스트 및 검증

```bash
make -C problem test
make -C problem run-py
```

fixture 테스트 결과: PASS

### 단계 4: 문서화

```bash
vi docs/concepts/dfs-visit-order.md
vi docs/concepts/edge-cases.md
```

### 사용 도구

- Python 3, `sys.setrecursionlimit`
- GNU Make (테스트 자동화)
- 1260 풀이를 기반으로 변형 (코드 재사용)

## 이 타임라인을 읽는 기준

- `docs/references/reproducibility.md`가 빠른 명령표라면, 이 문서는 어떤 순서로 문제를 읽고 구현과 검증을 확인했는지까지 남기는 장문 재현 기록이다.
- `알고리즘 수업 - 깊이 우선 탐색 1`에서는 `그래프 표현을 고르고 방문 순서를 안정적으로 제어하는 연습`를 실제 명령과 문서 흐름으로 다시 밟아 볼 수 있어야 학습 기록으로서 가치가 생긴다.
- 비슷한 유형을 다시 만났을 때 바로 적용할 수 있는 작은 판단 기준을 남겨 두는 것이 핵심이었다.

## 지금 다시 따라 할 때의 최소 순서

1. `problem/README.md`와 `docs/references/overview.md`로 문제 자료와 읽기 순서를 먼저 확인한다.
2. `make -C problem test`로 현재 구현이 fixture를 통과하는지 가장 먼저 본다.
3. `make -C problem run-py`로 대표 입력을 직접 따라가며 상태 전이를 확인한다.
4. `01-approach-log.md`, `02-debug-log.md`와 함께 읽으며 선택 이유와 실패 지점을 대조한다.

## 재현이 끝났는지 확인하는 질문

- 문서에 적힌 경로와 실제 실행 명령이 모두 맞는가?
- 자동 검증 결과와 수동 실행에서 본 상태 전이가 서로 모순되지 않는가?
- 같은 트랙의 다음 프로젝트로 넘어가기 전에 이번 선택 기준을 한 문장으로 요약할 수 있는가?

## 이어서 읽을 경로

- [`../docs/references/approach.md`](../docs/references/approach.md)
- [`../docs/references/reproducibility.md`](../docs/references/reproducibility.md)
- 앞 프로젝트: [`../../1260/README.md`](../../1260/README.md) (DFS와 BFS)
- 다음 프로젝트: [`../../7576/README.md`](../../7576/README.md) (토마토)
