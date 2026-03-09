# BOJ 2750 — 디버깅 기록

## 특이사항

로직이 단순해서 디버깅할 것이 거의 없었다.

## 유일한 주의점: 출력 형식

각 숫자를 한 줄씩 출력해야 한다. `print(nums)`로 리스트를 출력하면 안 됨.  
`'\n'.join(map(str, nums))`로 해결.

## 확인 과정

```bash
make -C problem test
```

PASS.
