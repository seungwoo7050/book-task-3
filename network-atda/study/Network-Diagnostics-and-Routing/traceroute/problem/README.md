# Traceroute 문제 안내

## 이 문서의 역할

이 문서는 `Traceroute`를 시작하기 전에 읽는 현재 저장소 기준 문제 사양입니다. 구현 세부와 공개 구현 경로는 상위 프로젝트 README가 연결하는 경로를 따라가면 됩니다.

## 문제 목표

TTL 값을 1씩 늘려 가며 UDP probe를 보내고, 돌아오는 ICMP 응답을 읽어 원격 호스트까지의 hop-by-hop 경로를 추적하는 작은 `traceroute` 도구를 구현합니다.

## 구현해야 할 동작

### Probe 전송

- TTL을 1부터 증가시키며 UDP probe를 보냅니다.
- 목적지 포트와 probe 식별 규칙을 정해 응답과 매칭할 수 있어야 합니다.

### ICMP 응답 처리

- 중간 라우터가 보낸 `ICMP Time Exceeded`를 식별합니다.
- 목적지에 도달했을 때 보통 돌아오는 `ICMP Port Unreachable`을 종료 조건으로 사용합니다.

### 매칭과 출력

- 수신한 ICMP 응답이 어떤 probe에 대한 것인지 판별합니다.
- hop 주소와 응답 시간을 traceroute 형식으로 출력합니다.

### 검증 분리

- live probing은 수동 재현 경로로 남기고, canonical test는 raw socket 없이 parser/formatter를 검증합니다.

## 제공 자료와 실행 환경

- starter code: `code/traceroute_skeleton.py`
- 실행 예시: `make run-client HOST=8.8.8.8`
- 정식 검증: `make test`

## 제약과 해석 기준

- Python 3 표준 라이브러리만 사용합니다.
- live 실행은 대부분의 시스템에서 elevated privileges가 필요합니다.
- `make test`는 raw socket을 열지 않는 deterministic 검증이어야 합니다.

## 성공 기준

| 항목 | 내용 |
| :--- | :--- |
| TTL 처리 | TTL 증가에 따라 hop을 순서대로 드러냅니다. |
| ICMP 파싱 | Time Exceeded와 Port Unreachable을 구분합니다. |
| Probe 매칭 | 응답과 probe를 정확히 연결합니다. |
| 출력 형식 | hop 주소와 지연을 읽기 쉽게 정리합니다. |
| 검증 구조 | live run과 deterministic test의 역할을 분리합니다. |
