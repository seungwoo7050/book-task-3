# BOJ 2920 — 접근 과정: 직접 비교

## 가장 단순한 구현

두 개의 고정 배열과 비교하는 것이 가장 명확하다:

```python
if nums == [1, 2, 3, 4, 5, 6, 7, 8]:
    print("ascending")
elif nums == [8, 7, 6, 5, 4, 3, 2, 1]:
    print("descending")
else:
    print("mixed")
```

## 대안으로 고려한 것

- **인접 원소 차이 검사**: `nums[i+1] - nums[i]`가 모두 1이면 ascending, 모두 -1이면 descending. 더 일반적이지만 이 문제에서는 과한 설계.
- **sorted 비교**: `nums == sorted(nums)` vs `nums == sorted(nums, reverse=True)`. 정렬의 오버헤드가 불필요.
- **all + zip**: `all(a < b for a, b in zip(nums, nums[1:]))`. Pythonic하지만 가독성이 떨어짐.

고정 입력이 8개뿐이므로 직접 비교가 가장 명확하고 효율적이다.
