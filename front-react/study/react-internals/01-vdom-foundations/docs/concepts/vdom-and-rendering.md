# VDOM 과 동기 렌더 흐름

이 단계의 핵심은 브라우저 DOM을 직접 만지기 전에 "원하는 UI를 데이터로 표현"한다는 점이다.

## VNode 구조

현재 구현의 최소 단위는 아래와 같다.

```ts
interface VNode {
  type: string | Function;
  props: {
    [key: string]: any;
    children: VNode[];
  };
}
```

이 구조가 주는 이점은 두 가지다.

- 트리 전체가 plain object라서 생성 비용이 싸다.
- 브라우저 API를 건드리지 않고도 old/new UI를 비교할 준비가 된다.

## 동기 렌더 순서

`render`는 아래 순서로 동작한다.

1. `createDom`으로 현재 VNode의 실제 DOM 노드를 만든다.
2. `updateDom`으로 prop과 이벤트를 반영한다.
3. child가 있으면 재귀적으로 같은 과정을 반복한다.
4. 마지막에 현재 DOM 노드를 부모 컨테이너에 append한다.

## `updateDom`의 순서가 중요한 이유

이 구현은 prop 업데이트를 네 단계로 나눈다.

1. 이전 이벤트 제거
2. 사라진 일반 prop 제거
3. 새 일반 prop 설정
4. 새 이벤트 추가

이 순서를 지키면 핸들러 중복 등록이나 오래된 prop 잔존을 줄일 수 있다.

## 이 단계의 한계

- 트리 전체를 매번 다시 렌더한다.
- 변경 집합을 계산하지 않는다.
- 큰 트리에서는 동기 재귀가 메인 스레드를 오래 점유한다.

이 한계가 다음 프로젝트 `02-tree-reconciliation`과 `03-fiber-scheduler`의 출발점이다.

