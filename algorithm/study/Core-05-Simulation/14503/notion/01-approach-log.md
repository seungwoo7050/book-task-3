# 접근 로그

> 프로젝트: 로봇 청소기
> 아래 내용은 `notion-archive/01-approach-log.md`에 남아 있던 기존 학습 기록을 현재 공개 노트 기준으로 다듬은 버전이다.

## 방향 인코딩

0=북, 1=동, 2=남, 3=서를 방향 벡터로 변환:

```python
dr = [-1, 0, 1, 0]  # 행 변화
dc = [0, 1, 0, -1]  # 열 변화
```

## 왼쪽 회전

"왼쪽으로 회전"은 방향 번호를 `(d + 3) % 4`로 변환한다. 
- 북(0) → 서(3), 서(3) → 남(2), 남(2) → 동(1), 동(1) → 북(0)

`+3`이 `−1`과 modular 상에서 동치임을 이용한 트릭.

## 후진

후진은 방향을 바꾸지 않고 반대 방향으로 한 칸 이동: `(d + 2) % 4`

## 메인 루프 구조

```python
while True:
    # 1. 현재 칸 청소
    if not cleaned[r][c]:
        cleaned[r][c] = True
        count += 1

    # 2. 4방향 회전 탐색
    found = False
    for _ in range(4):
        d = (d + 3) % 4
        nr, nc = r + dr[d], c + dc[d]
        if 범위 내 and 빈 칸 and 미청소:
            r, c = nr, nc
            found = True
            break

    if found: continue

    # 3. 후진 시도
    bd = (d + 2) % 4
    br, bc = r + dr[bd], c + dc[bd]
    if 벽이 아니면: r, c = br, bc
    else: break  # 종료
```

## cleaned vs grid

`grid`는 벽/빈칸 정보이고, `cleaned`는 청소 여부를 별도로 관리한다. grid를 변경하지 않는 것이 후진 시 벽 판별과의 혼동을 방지한다.
