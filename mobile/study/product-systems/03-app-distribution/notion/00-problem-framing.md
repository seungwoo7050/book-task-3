# Problem Framing — App Distribution

## 이 프로젝트는 어떤 질문에서 시작했나

앱을 만드는 것과 앱을 배포하는 것은 완전히 다른 일이다. `realtime-chat`에서 채팅 앱의 핵심 로직을 검증했지만, 그 앱이 실제로 사용자에게 전달되려면 환경 분리, 빌드 자동화, 서명 관리, CI/CD 파이프라인 같은 전혀 다른 영역의 문제를 풀어야 한다.

이 프로젝트는 그 "배포 규율(release discipline)"을 앱 코드와 분리해서 별도로 학습하는 과제다. 실제 스토어 업로드까지 가지 않되, **배포 준비가 되었는지를 검증하는 과정 자체**를 재현 가능하게 만드는 것이 목표다.

## 풀어야 했던 다섯 가지 문제

1. **앱 스냅샷 복사** — 검증된 `realtime-chat` 앱을 release candidate로 가져오기
2. **환경 분리** — `development`, `staging`, `production` 세 채널의 env 파일 구성
3. **Fastlane 설정** — iOS/Android 각각의 validation lane과 rehearsal lane 정의
4. **GitHub Actions 워크플로우** — typecheck, test, release validation을 자동화하는 CI 파이프라인
5. **로컬 리허설 명령** — `make release-rehearsal`로 요약 artifact를 재생성하는 자급 자족 프로세스

## 명시적으로 하지 않은 것

- 실제 App Store / Play Store 업로드
- 실제 서명 비밀(signing secrets) 저장소 투입
- App Center / CodePush를 이용한 OTA 업데이트
- 운영 환경 모니터링 인프라

## 이 과제가 학습 경로에서 차지하는 위치

`realtime-chat`이 "제품 동작"을 증명하는 프로젝트라면, `app-distribution`은 "배포 준비"를 증명하는 프로젝트다. 두 관심사를 분리함으로써, 제품 코드에 배포 설정이 섞이지 않고, 배포 학습에 제품 버그가 방해하지 않는 구조를 유지할 수 있었다.
