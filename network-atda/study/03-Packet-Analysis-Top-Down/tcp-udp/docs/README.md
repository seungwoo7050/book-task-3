# 개념 문서 안내

## 이 폴더의 역할
이 디렉터리는 `TCP and UDP Packet Analysis`를 공부할 때 반복해서 다시 볼 개념과 판단 근거만 남깁니다. 문제 이해의 출발점은 아니며, `problem/README.md`와 `analysis/README.md`를 읽은 뒤 필요한 문서만 다시 참조합니다.

## 먼저 볼 파일
- [`reproducibility.md`](concepts/reproducibility.md)
- [`tcp-flow-congestion.md`](concepts/tcp-flow-congestion.md)

## 기준 명령
- 기준 검증: `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`
- 개념 문서 위치: `docs/concepts/`
- 참고 자료 위치: `docs/references/`

## 현재 범위
- TCP의 신뢰성 메커니즘과 UDP의 단순성을 같은 전송 계층 시야에서 비교하는 랩입니다.

## 남은 약점
- 이 폴더만으로 문제와 답을 모두 이해할 수 있게 만들지 않습니다.
- 최신 공개 범위와 한계는 프로젝트 README를 기준으로 확인합니다.
