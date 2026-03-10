# Part C에서 보는 성능 모델의 의미

## Part C는 단순 최적화 문제가 아니다

Part C의 핵심은 "`ncopy`가 맞게 돌아간다"에서 끝나지 않습니다.
같은 의미를 유지하면서 pipeline이 덜 막히도록 instruction 배치를 바꾸는 것이 본질입니다.

## 저장소에서 pseudo-cost model을 둔 이유

공식 simulator는 로컬에 복원해서 돌릴 수 있지만, 공개 저장소 안에서 reasoning 자체를 읽기에는 불편합니다.
그래서 이 저장소는 baseline과 optimized 버전의 상대적 차이를 설명하는 간단한 pseudo-cost model을 함께 둡니다.

비교하고 싶은 것은 절대 cycle 수가 아니라 다음 사실입니다.

- optimized schedule의 pseudo-CPE가 baseline보다 낮다
- correctness는 그대로 유지된다

## 실제로 줄어드는 비용

최적화된 `ncopy`는 보통 다음 비용을 줄입니다.

- loop overhead
- branch 반복 횟수
- 불필요한 의존성으로 인한 pipeline stall

그래서 Part C는 "더 짧게 쓰기"가 아니라 "더 덜 막히게 배치하기" 문제로 보는 편이 정확합니다.

## 공식 결과와 companion model의 관계

- 공식 결과는 로컬 복원 toolchain에서 확인한다
- companion model은 그 결과를 이해하기 위한 설명 도구다

두 경로가 함께 있을 때, 공개 저장소도 읽기 쉽고 실제 검증도 가능해집니다.
