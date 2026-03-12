# Problem: App Distribution

> Status: VERIFIED
> Scope: modern RN release rehearsal
> Last Checked: 2026-03-12

## 문제 요약

검증된 `realtime-chat` snapshot을 release candidate로 가져와,
실제 credential을 저장소에 넣지 않고도 packaging, env separation, automation rehearsal을 증명하는 과제다.

## 왜 이 문제가 커리큘럼에 필요한가

제품 동작과 release discipline은 다른 문제다.
이 프로젝트는 "앱이 동작하는 것"에서 멈추지 않고, 배포 전 점검까지 결과물로 남길 수 있는가를 확인한다.

## 제공 자료

- `realtime-chat` verified snapshot
- `problem/code/README.md`의 release scaffold
- `problem/data/README.md`의 보조 자료

## 필수 요구사항

1. release candidate 복제
2. `development`, `staging`, `production` 환경 분리
3. Fastlane lane 구성
4. GitHub Actions workflow 추가
5. local rehearsal command와 summary artifact 생성

## 의도적 비범위

- 실제 App Store / Play Store 업로드
- signing secret 저장
- OTA update 인프라 도입

## 평가/검증 기준

```bash
make test
make app-build
make app-test
make release-rehearsal
```

- private credential 없이 네 명령이 모두 재현 가능해야 한다.
- release rehearsal이 요약 artifact를 남겨야 한다.
- env separation이 문서와 예시 파일로 드러나야 한다.

## 원문/출처 보존 위치

- [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
