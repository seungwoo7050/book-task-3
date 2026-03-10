# 0x16 Computational Geometry — 디버깅 기록

## Collinear 엣지 케이스

두 선분이 일직선 위에 있으면서 겹치지 않는 경우, cross product만으로는 교차로 잘못 판단. `on_segment` 추가 검사 필수.

## Convex Hull 중복 점

동일 좌표 점이 여러 개면 hull 결과에 중복 포함 가능. 정렬 후 자연 처리.

## 테스트

```bash
make -C problem test
```

PASS.
