# 00. 문제 정의

## 문제를 어떻게 이해했는가

`proxylab`은 단순 소켓 과제가 아니라,
"한 요청을 다른 서버로 안전하게 넘기고, 동시에 여러 요청을 처리하며, 공용 cache를 유지하는 법"을 묻는 프로젝트라고 봤다.

## 저장소 기준 성공 조건

- absolute-form `GET`를 파싱한다
- outbound request를 `HTTP/1.0` 기준으로 다시 쓴다
- thread-per-connection 모델이 동작한다
- small object cache hit를 재현한다
- local origin harness로 기능과 동시성을 검증한다

## 선수 지식

- socket API와 robust I/O
- HTTP/1.0 요청 형식
- thread와 mutex
- LRU cache 기본 개념
