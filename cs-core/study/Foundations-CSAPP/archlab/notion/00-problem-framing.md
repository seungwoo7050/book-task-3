# 00. 문제 정의

## 문제를 어떻게 이해했는가

`archlab`은 하나의 랩 이름 아래 세 종류의 산출물을 요구한다.

- Part A: Y86-64 어셈블리
- Part B: HCL 제어 로직
- Part C: pipeline 성능 최적화

그래서 이 저장소도 처음부터 "한 디렉터리에 다 넣지 않는다"는 방향으로 구조를 잡았다.

## 저장소 기준 성공 조건

- `y86/`에 공식 hand-in 성격 산출물이 남는다
- `c/`, `cpp/`에 의미 보조 모델이 남는다
- `problem/`에서 공식 self-study toolchain 복원 경로가 유지된다
- 공개 문서만 읽어도 Part A/B/C 관계가 보인다

## 선수 지식

- Y86-64 기본 명령 집합
- condition code와 `iaddq` 의미
- pipeline hazard와 throughput
- `ncopy` 최적화 목적
