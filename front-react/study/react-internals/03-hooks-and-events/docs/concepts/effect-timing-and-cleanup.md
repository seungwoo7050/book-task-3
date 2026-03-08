# Effect Timing And Cleanup

`useEffect`는 render phase에서 바로 실행되지 않는다. 이 runtime은 render가 끝난 뒤 commit이 끝난 다음에 effect setup을 실행한다.

## 흐름

1. render phase에서 effect registration만 기록한다.
2. commit이 끝난 뒤에 이전 cleanup을 실행한다.
3. 그 다음 새 effect setup을 실행한다.
4. component가 사라지면 unmount cleanup을 실행한다.

## 범위

- dependency array 비교는 최소 동등성 비교만 지원한다.
- layout effect와 insertion effect는 없다.
- React의 모든 edge case를 재현하지는 않는다.
