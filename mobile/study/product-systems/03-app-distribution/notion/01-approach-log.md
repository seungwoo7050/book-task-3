# Approach Log — App Distribution

## 첫 번째 결정: realtime-chat 앱을 복사할 것인가, 참조할 것인가

두 가지 선택지가 있었다. `realtime-chat`을 심볼릭 링크나 npm workspace로 참조하거나, 파일을 통째로 복사하거나.

복사를 택했다. 이유는 세 가지다:
1. 배포 프로젝트가 제품 프로젝트의 변경에 영향받지 않아야 한다
2. package.json의 scripts 섹션을 배포 전용으로 확장할 수 있어야 한다
3. 독립적인 `.env` 파일과 Fastlane 설정을 가져야 한다

복사 과정에서 `chatModel.ts`, `storageSchema.ts`, `RealtimeChatStudyApp.tsx`를 그대로 가져오고, 여기에 `releasePlan.ts`를 추가했다.

## 두 번째 결정: 환경 분리를 어떻게 구현할 것인가

`react-native-config` 같은 라이브러리를 도입할 수도 있었지만, 이 프로젝트에서는 `.env.*.example` 파일과 검증 스크립트의 조합으로 구현했다.

세 채널 모두 동일한 키 집합(`API_BASE_URL`, `WS_BASE_URL`, `RELEASE_CHANNEL`, `SENTRY_DSN`)을 가지도록 강제하는 `validate-release.mjs` 스크립트를 만들었다. 키가 하나라도 어긋나면 검증이 실패한다.

이 방식의 장점은 네이티브 빌드 설정을 건드리지 않으면서도 "환경별로 동일한 설정 구조를 유지한다"는 원칙을 코드로 증명할 수 있다는 것이다.

## 세 번째 결정: Fastlane lane을 어떤 수준까지 정의할 것인가

실제 빌드나 서명 없이 Fastlane을 사용하는 것이 이 프로젝트의 핵심 제약이다. 그래서 각 lane은 `validate_env` (env 검증 스크립트 실행) + echo (dry-run 메시지) 구조로 만들었다.

iOS에는 `validate_env`, `rehearsal_staging`, `rehearsal_production` 세 lane, Android에도 동일한 세 lane을 정의했다. 모든 rehearsal lane은 `validate_env`를 먼저 호출한 뒤 dry-run 메시지를 출력한다.

이 설계는 "실제 빌드 인프라가 갖춰지면, echo 부분만 실제 빌드 명령으로 바꾸면 된다"는 확장 포인트를 남겨둔 것이다.

## 네 번째 결정: GitHub Actions 워크플로우 범위

워크플로우는 `typecheck → test → release:validate` 세 단계만 포함한다. 실제 빌드나 배포 단계는 의도적으로 빠져 있다.

트리거는 `workflow_dispatch`(수동)와 `pull_request`(app-distribution 경로 변경 시)로 설정했다. 이렇게 하면 이 디렉토리의 코드가 바뀔 때만 CI가 돌아간다.

## 다섯 번째 결정: 리허설 요약(rehearsal-summary.json)을 왜 만드는가

`release-rehearsal.mjs`는 env 검증, Fastlane 존재 확인, 워크플로우 존재 확인을 한 번에 실행하고 결과를 `release/rehearsal-summary.json`에 기록한다. 이 JSON 파일이 존재한다는 것 자체가 "로컬에서 배포 준비 검증을 성공적으로 실행했다"는 증거다.

이 아이디어는 `virtualized-list`의 `benchmark-summary.json`과 같은 패턴이다 — 검증 결과를 재현 가능한 artifact로 남기는 것.
