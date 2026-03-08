# 공개 답안 안내

이 디렉터리는 `TCP and UDP Packet Analysis`의 공개 답안과 근거 문서를 담는다.

## 구성

- `src/tcp-udp-analysis.md`

## 기준 명령

- 검증: `make -C study/Packet-Analysis-Top-Down/tcp-udp/problem test`
- 원문에서 영어 답안을 요구한 랩은 답안도 영어로 유지한다.

## 분석 원칙

- 관찰 가능한 trace evidence만 사용한다.
- 관찰 불가한 항목은 명시적으로 남긴다.
- 주장마다 packet/frame number와 field value를 연결한다.
