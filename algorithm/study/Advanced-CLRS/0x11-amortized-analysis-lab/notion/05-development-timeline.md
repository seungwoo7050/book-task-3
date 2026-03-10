# 개발 타임라인

> 프로젝트: 상각 분석 실습
> 이 문서는 학습자가 현재 저장소 기준으로 구현과 검증 과정을 끝까지 다시 밟아 볼 수 있게 정리한 재현 문서다.

## 왜 이 문서가 중요한가

- `docs/references/reproducibility.md`는 빠른 실행 명령을 확인하는 문서이고, 여기서는 그 명령을 어떤 순서와 맥락에서 실행했는지까지 남긴다.
- 학습 레포에서 재현성은 '명령 하나를 안다'가 아니라 '어떤 문서를 읽고 어떤 확인을 거쳐 현재 구현에 도달하는지 따라갈 수 있다'는 뜻에 더 가깝다.

## 재현 시작점

- 현재 기준 경로: `study/Advanced-CLRS/0x11-amortized-analysis-lab`
- 먼저 확인할 빠른 명령: `make -C problem test`
- 함께 읽을 빠른 문서: `../docs/references/reproducibility.md`, `01-approach-log.md`, `02-debug-log.md`

## 단계별 기록

아래 메모는 `notion-archive/05-development-timeline.md`의 실제 기록을 현재 공개 노트 기준으로 다듬고, 지금 다시 따라 할 때 필요한 설명을 덧붙인 버전이다.

### 단계 1: 프로젝트 스캐폴딩

자체 제작. STACK/COUNTER 두 모드 fixture 생성.

### 단계 2: Python 구현

Stack MULTIPOP + Binary Counter 비용 추적.

### 단계 3: 테스트

```bash
make -C problem test
```

PASS.

### 사용 도구

- Python 3
- GNU Make

## 이 타임라인을 읽는 기준

- `docs/references/reproducibility.md`가 빠른 명령표라면, 이 문서는 어떤 순서로 문제를 읽고 구현과 검증을 확인했는지까지 남기는 장문 재현 기록이다.
- `상각 분석 실습`에서는 `상각 분석 실습의 핵심 아이디어를 작은 실험과 자동 검증으로 다시 설명하는 연습`를 실제 명령과 문서 흐름으로 다시 밟아 볼 수 있어야 학습 기록으로서 가치가 생긴다.
- CLRS Ch 17의 핵심 아이디어를 입출력과 자동 검증이 가능한 작은 실험으로 바꾸는 과정이 중요했다.

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
- 앞 프로젝트: [`../../0x10-strassen-matrix/README.md`](../../0x10-strassen-matrix/README.md) (Strassen 행렬 곱셈)
- 다음 프로젝트: [`../../0x12-red-black-tree/README.md`](../../0x12-red-black-tree/README.md) (레드-블랙 트리 삽입과 검증)
