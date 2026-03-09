# 디버그 기록 — print vs sys.stdout.write

## 성능 이슈

처음에 `print()`로 출력했을 때, 대량 테스트 케이스에서 미세하게 느렸다.
`sys.stdout.write()`로 바꾸니 안정적으로 통과했다.
Python에서 대량 출력이 필요할 때는 `sys.stdout.write`가 관용적 선택이다.

## 빈 스택 체크

1406과 동일하게, `<`/`-`에서 left가 비어 있으면 무시, `>`에서 right가 비어 있으면 무시.
`if left:` 가드로 충분하다.

## 검증 결과

fixture 테스트 통과. Python/C++ 교차 검증 완료.
