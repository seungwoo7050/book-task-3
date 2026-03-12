# Native Modules

Status: verified

## 한 줄 답

Battery, Haptics, Sensor 세 모듈의 TypeScript spec과 codegen summary, consumer screen을 묶어 JS/native boundary를 설명한 프로젝트다.

## 무슨 문제를 풀었나

native module 학습은 종종 플랫폼별 구현 예제만 남고 public contract가 흐려진다.
이 프로젝트의 질문은 "모듈 경계를 어떤 spec과 문서로 고정해야 JS/native boundary를 재현 가능하게 설명할 수 있는가"다.

## 내가 만든 답

- Battery, Haptics, Sensor 모듈의 typed spec을 정의했다.
- codegen summary export를 추가했다.
- consumer screen에서 각 모듈의 사용 패턴을 시연했다.
- platform parity와 boundary 판단 기준을 문서화했다.

## 무엇이 동작하나

- typed module specs
- codegen summary export
- consumer app screen
- platform parity 문서

## 검증 명령

```bash
make -C study/architecture/02-native-modules/problem test
make -C study/architecture/02-native-modules/problem codegen
make -C study/architecture/02-native-modules/problem app-build
make -C study/architecture/02-native-modules/problem app-test
```

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [react-native/README.md](react-native/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 학습 포인트

- native boundary를 "기능 구현"보다 "public contract 설계"로 보기
- codegen 결과를 결과물의 일부로 남기기
- 플랫폼 차이를 문서로 설명 가능한 수준까지 끌어올리기

## 현재 상태

- 문제 정의: `verified`
- RN 구현: `verified`
- codegen/문서: `verified`
