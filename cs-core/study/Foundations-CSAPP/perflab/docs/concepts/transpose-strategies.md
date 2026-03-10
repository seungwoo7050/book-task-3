# matrix transpose는 왜 크기마다 전략이 달라지는가

## 같은 문제인데 왜 세 전략이 필요한가

transpose는 겉으로는 항상 같은 연산입니다.
하지만 direct-mapped cache에서는 행렬 크기에 따라 conflict miss 양상이 크게 달라집니다.

| 크기 | 주된 문제 | 저장소에서 쓰는 전략 |
|---|---|---|
| `32x32` | diagonal conflict | `8x8` blocking + diagonal 지연 쓰기 |
| `64x64` | 단순 `8x8` 재사용 시 심한 conflict | quadrant를 나눈 `8x8` 스케줄 |
| `61x67` | 가장자리 처리와 비정형 크기 | `16x16` block + guard |

## 왜 `64x64`가 특히 까다로운가

`32x32`에서 잘 먹히는 단순 block 전략을 그대로 쓰면,
`64x64`에서는 같은 set 충돌이 과하게 반복됩니다.

그래서 Part B의 핵심은 "block을 쓴다"가 아니라
"그 block 안에서 읽기/쓰기 순서를 어떻게 배치할 것인가"에 가깝습니다.

## 이 저장소의 benchmark 기준

`study/` 구현은 wall-clock time 대신 miss count를 봅니다.
이유는 다음과 같습니다.

- 재현 가능하다
- 머신 성능 차이 영향을 덜 받는다
- 과제가 실제로 배우게 하려는 것도 locality reasoning이다

검증 기준은 다음 세 가지입니다.

- 정답 행렬이 맞는가
- naive보다 miss가 줄었는가
- 공식 임계치에 근접하거나 넘는가
