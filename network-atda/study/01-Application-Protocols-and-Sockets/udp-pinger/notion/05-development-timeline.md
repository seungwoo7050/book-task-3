# 05 개발 타임라인

이 문서는 `UDP Pinger`를 처음 따라가는 학생을 위한 재현 가이드다. 자동 테스트와 수동 실행을 둘 다 거치면서, 손실이 있어도 프로그램이 끝까지 동작해야 한다는 점을 직접 확인하는 데 목적이 있다.

## 준비
- `python3`
- `pytest`
- 작업 위치: 저장소 루트 `/Users/woopinbell/work/book-task-3/network-atda`

## 단계 1. 문제와 제공물 확인
먼저 아래 파일을 읽는다.
- [`../problem/README.md`](../problem/README.md)
- [`../problem/code/udp_pinger_server.py`](../problem/code/udp_pinger_server.py)
- [`../problem/code/udp_pinger_client_skeleton.py`](../problem/code/udp_pinger_client_skeleton.py)

여기서 확인할 질문:
- 왜 서버가 일부 패킷을 일부러 버리는가
- 응답 본문이 왜 대문자로 바뀌는가
- 검증은 몇 번의 ping과 어떤 통계로 끝나는가

## 단계 2. 현재 구현과 테스트를 연결해 본다
- [`../python/src/udp_pinger_client.py`](../python/src/udp_pinger_client.py)
- [`../python/tests/test_udp_pinger.py`](../python/tests/test_udp_pinger.py)

이 단계에서는 다음만 보면 충분하다.
- timeout을 어디서 처리하는가
- RTT 목록과 손실 개수를 어떻게 따로 관리하는가
- 응답 본문과 RTT 계산이 왜 분리되어 있는가

## 단계 3. 자동 검증 먼저 실행
아래 명령으로 제공 서버와 솔루션 클라이언트를 함께 검증한다.

```bash
make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem test
```

기대 결과:
- 임시 UDP 서버가 뜬다.
- 클라이언트가 전체 10회를 끝까지 수행한다.
- 응답 성공, 대문자 응답, timeout 처리가 모두 검증된다.

세부 테스트를 보고 싶다면 아래도 실행한다.

```bash
cd study/01-Application-Protocols-and-Sockets/udp-pinger/python/tests
python3 -m pytest test_udp_pinger.py -v
```

## 단계 4. 수동으로 RTT와 손실을 직접 본다
터미널 1:

```bash
make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem run-server
```

터미널 2:

```bash
make -C study/01-Application-Protocols-and-Sockets/udp-pinger/problem run-solution
```

기대 결과:
- `PING` 출력이 10회 나온다.
- 일부는 `Request timed out`처럼 손실로 기록될 수 있다.
- 성공한 응답은 RTT와 함께 출력된다.
- 마지막에 최소/최대/평균 RTT와 손실 개수 요약이 나온다.

## 단계 5. 실패하면 가장 먼저 볼 곳
- 전부 timeout이면 서버가 정말 떠 있는지와 호스트/포트를 먼저 확인한다.
- 평균 RTT 계산이 이상하면 성공 샘플만 집계하는지 먼저 본다.
- 응답 문자열 비교가 꼬이면 서버가 대문자 변환을 한다는 점을 다시 확인한다.
- 관련 근거는 [`02-debug-log.md`](02-debug-log.md)에 정리했다.

## 단계 6. 완료 판정
아래 조건을 만족하면 이 프로젝트는 재현한 것으로 본다.
- 제공 서버와 현재 구현의 역할 차이를 설명할 수 있다.
- `make test`가 통과한다.
- 수동 실행에서 손실이 있어도 프로그램이 끝까지 종료된다.
- RTT 통계에서 왜 손실 샘플을 제외하는지 설명할 수 있다.
