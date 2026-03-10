# 03. 회고

## 이번 프로젝트에서 크게 남은 교훈

셸은 작은 프로그램처럼 보이지만,
실제로는 "누가 언제 상태를 바꾸는가"를 이해하는 프로젝트였다.

특히 다음이 오래 남는다.

- signal handler와 메인 루프가 같은 상태 모델을 공유해야 한다
- process group을 이해해야 job control이 설명된다
- self-owned 테스트가 없으면 signal 버그는 금방 숨는다

## 저장소 차원에서 잘한 결정

- 공식 starter 제거 사실을 `problem/`에 명확히 남겼다
- 공개 검증 경로를 self-owned harness로 옮겼다
- README와 `docs/`가 race 중심으로 읽히게 정리했다
