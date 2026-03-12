# App Distribution

Status: verified

## 한 줄 답

`realtime-chat`의 verified snapshot을 release candidate로 삼아 env separation, Fastlane, GitHub Actions, local rehearsal까지 닫은 배포 리허설 프로젝트다.

## 무슨 문제를 풀었나

동작하는 앱이 있어도 release discipline이 없으면 제품형 결과물로 보기 어렵다.
이 프로젝트의 질문은 "실제 credential dump 없이도 packaging과 rehearsal automation을 저장소 안에서 증명할 수 있는가"다.

## 내가 만든 답

- `realtime-chat` snapshot을 release candidate로 복사했다.
- `development`, `staging`, `production` env separation을 추가했다.
- Fastlane lane과 GitHub Actions workflow를 구성했다.
- local release rehearsal command와 summary artifact를 만들었다.

## 무엇이 동작하나

- env example 파일
- Fastlane validation / signing rehearsal / archive dry-run
- GitHub Actions release workflow
- local rehearsal summary 생성

## 검증 명령

```bash
make -C study/product-systems/03-app-distribution/problem test
make -C study/product-systems/03-app-distribution/problem app-build
make -C study/product-systems/03-app-distribution/problem app-test
make -C study/product-systems/03-app-distribution/problem release-rehearsal
```

## 읽는 순서

1. [problem/README.md](problem/README.md)
2. [react-native/README.md](react-native/README.md)
3. [docs/README.md](docs/README.md)
4. [notion/README.md](notion/README.md)

## 학습 포인트

- 제품 동작 검증과 release rehearsal을 분리하기
- 비밀정보 없이도 배포 준비 상태를 설명하기
- 배포 자동화를 결과물의 일부로 남기기

## 현재 상태

- 문제 정의: `verified`
- RN 구현: `verified`
- release rehearsal 자산: `verified`
