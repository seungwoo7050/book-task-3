# 학습 문서 안내

## 이 폴더의 역할

이 폴더는 이 프로젝트를 읽을 때 반복해서 다시 볼 판단 근거만 남긴다. 문제 이해의 출발점은 프로젝트 README이고, 이 폴더는 답을 왜 그렇게 골랐는지 확인하는 보조 표면이다.

## 먼저 볼 파일

- [references/approach.md](references/approach.md)
- [references/reproducibility.md](references/reproducibility.md)
- [concepts/edge-cases.md](concepts/edge-cases.md)
- [concepts/meldable-heap-concept.md](concepts/meldable-heap-concept.md)

## 기준 명령

- 기준 검증: `make -C study/Advanced-CLRS/0x13-meldable-heap/problem test`
- 개념 문서 위치: `docs/concepts/`
- 참고 문서 위치: `docs/references/`

## 현재 범위

- 한 줄 답: `python/src/solution.py`에서 `합칠 수 있는 힙 브리지` 핵심 절차를 실행 가능한 실험으로 재현

## 남은 약점

- 이 폴더만으로 문제와 구현을 모두 이해하게 만들지는 않는다.
- 프로젝트 전체 맥락과 경로는 상위 README를 기준으로 확인한다.
