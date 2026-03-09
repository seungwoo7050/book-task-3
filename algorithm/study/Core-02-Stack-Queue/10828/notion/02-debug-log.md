# 디버그 기록

## 유일한 주의점
비어 있는 스택에서 pop/top 시 `-1`을 출력해야 한다. Python의 빈 리스트에서 `pop()`을 호출하면 IndexError가 나므로, `if stack:` 가드가 필수.

## 검증 결과
fixture 테스트 통과.
