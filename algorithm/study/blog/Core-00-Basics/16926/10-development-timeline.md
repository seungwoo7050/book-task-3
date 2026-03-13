# BOJ 16926 — 개발 타임라인 (전반)

## Phase 1
### Session 1
- 목표: N×M 배열을 R번 반시계 방향으로 회전시킨다.
- 진행: 처음엔 배열 전체를 한 번에 회전시키려 했다. 그런데 바깥 테두리와 안쪽 테두리는 독립적으로 회전한다는 걸 깨달았다.
- 이슈: 행렬이 직사각형이라 각 레이어(양파 껍질처럼 벗기는 테두리)의 길이가 다르다.
- 판단: 레이어 분해 방식을 쓴다. 각 레이어를 1차원 리스트로 펼치고, R만큼 시프트하고, 다시 2차원에 채운다.

### Session 2
- 목표: 레이어 추출과 시프트를 구현한다.

이 시점의 핵심 코드:

```python
layers = min(N, M) // 2
for k in range(layers):
    ring = []
    for j in range(k, M - k):
        ring.append(arr[k][j])
    for i in range(k + 1, N - k):
        ring.append(arr[i][M - 1 - k])
    for j in range(M - 2 - k, k - 1, -1):
        ring.append(arr[N - 1 - k][j])
    for i in range(N - 2 - k, k, -1):
        ring.append(arr[i][k])
```

이 코드가 까다로운 이유는 테두리를 시계 방향으로 순회하면서 1차원 리스트에 담아야 하기 때문이다. 윗줄 → 오른쪽 열 → 아랫줄(역순) → 왼쪽 열(역순) 순서로 네 변을 돌면서 모은다. 처음엔 코너가 중복으로 들어가서 ring 길이가 맞지 않았다.

- 이슈: R이 ring 길이보다 클 수 있으니까 `r = R % len(ring)`으로 모듈러를 해야 한다. 안 하면 시간 초과.

CLI:

```bash
$ make -C study/Core-00-Basics/16926/problem run-py
```

```text
2 1 8
3 2 7
4 3 6
5 4 5
```

- 다음: 다시 2차원에 써넣는 순서가 추출 순서와 정확히 같은지 확인한다.
