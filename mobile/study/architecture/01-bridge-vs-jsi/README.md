# Bridge Vs JSI

Status: verified

## 한 줄 답

RN 0.84 기준으로 legacy/new runtime 토글 대신 async serialized surface와 sync direct-call surface를 같은 workload로 비교한 benchmark 프로젝트다.

## 무슨 문제를 풀었나

RN architecture 설명은 쉽게 추상론이 된다.
이 프로젝트의 질문은 "bridge-like interop와 JSI-like direct call의 차이를 지금 버전의 RN에서 어떻게 계측하고 설명할 수 있는가"다.

## 내가 만든 답

- async interop-style surface와 sync direct-call surface를 같은 payload로 실행했다.
- 5회 반복 측정과 통계 요약을 추가했다.
- dashboard와 JSON export를 만들어 결과를 저장소에 남겼다.
- 왜 runtime toggle이 아니라 surface benchmark를 쓰는지 문서에 정리했다.

## 무엇이 동작하나

- async/sync benchmark 실행
- 평균/표준편차 요약
- benchmark dashboard
- deterministic JSON export

## 검증 명령

```bash
make -C study/architecture/01-bridge-vs-jsi/problem test
make -C study/architecture/01-bridge-vs-jsi/problem app-build
make -C study/architecture/01-bridge-vs-jsi/problem app-test
```

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [react-native/README.md](react-native/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 학습 포인트

- runtime 논의를 추상적인 개념 비교가 아니라 workload 비교로 바꾸기
- RN 버전 변화에 맞춰 benchmark 질문을 재정의하기
- architecture 문서를 결과물과 연결해 두기

## 현재 상태

- 문제 정의: `verified`
- RN 구현: `verified`
- benchmark 문서: `verified`
