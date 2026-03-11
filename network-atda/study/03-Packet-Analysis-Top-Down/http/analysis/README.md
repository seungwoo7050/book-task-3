# 공개 답안 안내

## 이 폴더의 역할
이 디렉터리는 `HTTP Packet Analysis`의 공개 답안과 핵심 근거 문서를 담습니다. 프로젝트 README에서 문제를 확인한 뒤, 실제 답은 여기서 읽습니다.

## 먼저 볼 파일
- `analysis/src/http-analysis.md` - 질문별 답안과 근거를 확인합니다.

## 기준 명령
- 검증: `make -C study/03-Packet-Analysis-Top-Down/http/problem test`

## 현재 범위
기본 GET, conditional GET, 긴 문서 전송, embedded object 요청을 패킷 수준에서 추적하는 랩입니다.

## 남은 약점
- `HTTP/2` 이상은 다루지 않습니다.
- 브라우저별 헤더 차이는 관찰 범위 밖입니다.
- 실시간 캡처 대신 고정 trace에 기반합니다.
