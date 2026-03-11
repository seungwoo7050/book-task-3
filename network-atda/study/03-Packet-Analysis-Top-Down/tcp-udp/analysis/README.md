# 공개 답안 안내

## 이 폴더의 역할
이 디렉터리는 `TCP and UDP Packet Analysis`의 공개 답안과 핵심 근거 문서를 담습니다. 프로젝트 README에서 문제를 확인한 뒤, 실제 답은 여기서 읽습니다.

## 먼저 볼 파일
- `analysis/src/tcp-udp-analysis.md` - 질문별 답안과 근거를 확인합니다.

## 기준 명령
- 검증: `make -C study/03-Packet-Analysis-Top-Down/tcp-udp/problem test`

## 현재 범위
TCP의 신뢰성 메커니즘과 UDP의 단순성을 같은 전송 계층 시야에서 비교하는 랩입니다.

## 남은 약점
- trace가 짧아 전체 congestion window evolution을 직접 보기는 어렵습니다.
- teardown과 장기 혼잡 제어 관찰은 제한적입니다.
