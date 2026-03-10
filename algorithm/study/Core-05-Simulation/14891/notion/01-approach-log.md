# 접근 로그

> 프로젝트: 톱니바퀴
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 자료구조 선택: deque

톱니바퀴의 회전을 deque로 구현한다:
- **시계 방향**: 마지막 원소를 꺼내서 앞에 넣기 (`appendleft(pop())`)
- **반시계 방향**: 첫 원소를 꺼내서 뒤에 넣기 (`append(popleft())`)

```python
gears = [deque(int(c) for c in input().strip()) for _ in range(4)]
```

## 전파 로직

핵심 설계: **전파 방향을 먼저 결정**한 후, **한 번에 회전 적용**.

```python
dirs = [0] * 4
dirs[num] = d

# 왼쪽 전파
for i in range(num - 1, -1, -1):
    if gears[i][2] != gears[i + 1][6]:
        dirs[i] = -dirs[i + 1]
    else:
        break

# 오른쪽 전파
for i in range(num + 1, 4):
    if gears[i][6] != gears[i - 1][2]:
        dirs[i] = -dirs[i - 1]
    else:
        break
```

`break`가 중요하다 — 중간에 접점이 같으면 그 이후로는 전파되지 않는다.

## 회전 적용

```python
for i in range(4):
    if dirs[i] == 1:
        gears[i].appendleft(gears[i].pop())
    elif dirs[i] == -1:
        gears[i].append(gears[i].popleft())
```

## 점수 계산

```python
score = sum(gears[i][0] * (1 << i) for i in range(4))
```

12시 방향(인덱스 0)의 톱니가 S극(1)이면 점수에 $2^i$를 더한다.

## 대안으로 고려한 것

- **리스트 슬라이싱**: `gear = gear[-1:] + gear[:-1]` — 매번 새 리스트를 생성하므로 비효율적
- **인덱스 오프셋**: 회전을 실제로 하지 않고, 현재 0번 인덱스의 오프셋만 관리. 효율적이지만 코드가 복잡해짐
