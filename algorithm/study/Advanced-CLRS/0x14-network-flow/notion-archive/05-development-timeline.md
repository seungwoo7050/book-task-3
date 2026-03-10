# 0x14 Network Flow — 개발 타임라인

## Phase 1: 그래프 입력

용량 행렬 + 인접 리스트 구축. 역간선 포함.

## Phase 2: BFS 증가 경로

parent 배열로 경로 추적, bottleneck 계산.

## Phase 3: 유량 갱신 루프

cap 갱신 반복, 총 유량 누적.

## Phase 4: 테스트

```bash
make -C problem test
```

PASS.

## 사용 도구

- Python 3
- GNU Make
