# Problem Guide

headless simulation만으로 rollback을 설명하는 프로젝트다. 여기서 핵심은 "입력이 늦게 도착했을 때 어느 시점으로 되돌아가야 하는가"이지, 서버 소켓을 여는 것이 아니다.

## 요구 사항

- frame-stamped input을 저장할 수 있어야 한다.
- 아직 오지 않은 입력은 이전 frame의 applied input을 이용해 locally predict해야 한다.
- 이미 지난 frame의 입력이 뒤늦게 도착하면 해당 frame부터 현재 frame까지 rollback / resimulation 해야 한다.
- replay가 끝난 뒤 같은 입력 세트를 다시 굴렸을 때 같은 상태가 나오는지 확인해야 한다.

## 성공 기준

- future input fast path
- late input rollback
- no-op late input fast path
- two-player resimulation convergence

이 네 경계가 테스트로 고정돼야 한다.

## 제공 자료

- `problem/data/late-input-timeline.txt`: rollback이 왜 필요한지 설명하는 간단한 시나리오 메모
