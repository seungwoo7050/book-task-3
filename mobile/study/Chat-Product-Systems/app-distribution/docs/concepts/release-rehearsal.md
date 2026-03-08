# Release Rehearsal

이 프로젝트의 리허설은 실제 store upload를 수행하지 않는다.
대신 아래 네 가지를 검증한다.

1. env 예시 파일이 모두 존재하고 동일한 키 집합을 가진다.
2. Fastlane lane 정의가 iOS/Android rehearsal 범위를 설명한다.
3. GitHub Actions workflow가 typecheck, test, rehearsal validation을 호출한다.
4. 로컬에서 `release/rehearsal-summary.json`을 재생성할 수 있다.

이 방식은 공개 저장소에서 비밀값 없이도 release discipline을 학습하게 해 준다.
