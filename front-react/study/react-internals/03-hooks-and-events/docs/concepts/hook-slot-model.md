# Hook Slot Model

이 단계의 hook 구현은 "호출 순서에 따라 slot array를 읽고 쓴다"는 가장 작은 모델을 택한다.

## 핵심 규칙

- 같은 component path는 같은 slot array를 재사용한다.
- 같은 render에서는 hook 호출 순서가 바뀌면 안 된다.
- `useState`와 `useEffect`는 각각 자신의 slot kind를 가진다.

## 왜 이 모델이 중요한가

hooks 규칙을 "외워야 하는 문법"으로 보면 금방 흐려진다. 반대로 slot array 관점으로 보면 왜 conditional hook이 깨지는지 바로 설명된다. 이번 구현도 hook count가 달라지면 런타임이 즉시 에러를 던지도록 했다.
