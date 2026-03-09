# BOJ 11725 — 디버깅 기록

## 주의점: 양방향 인접 리스트

트리 간선을 양방향으로 넣어야 한다. 입력이 `u v` 형태로 부모-자식 방향이 아닌 무방향 간선.

## 주의점: I/O 속도

$N \leq 100,000$. `sys.stdout.write` + `'\n'.join` 조합 사용.

## 확인 과정

```bash
make -C problem test
```

PASS.
