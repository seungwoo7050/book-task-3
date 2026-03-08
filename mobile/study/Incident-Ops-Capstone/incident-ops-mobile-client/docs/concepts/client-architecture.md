# Client Architecture

이 앱은 서버 계약을 바꾸지 않고 React Native 클라이언트 경계를 명확히 보여주는 데 초점을 둔다.

## Boundaries

- `problem/code/contracts/`: 서버와 공유하는 공용 DTO/도메인 타입
- `react-native/src/lib/api.ts`: HTTP/WS 경계
- `react-native/src/lib/storage.ts`: 세션, 설정, outbox 영속화
- `react-native/src/lib/outbox.ts`: 앱 로컬 optimistic state와 retry/DLQ 규칙
- `react-native/src/app/AppModel.tsx`: 화면에서 사용하는 조합 계층

## Why Local View Models Exist

공용 계약에는 UI 상태를 넣지 않는다.
대신 다음 값은 앱 로컬 타입으로만 유지한다.

- connection 상태
- stream 연결 상태
- queued mutation 메타데이터
- optimistic incident list item

이 분리는 서버 계약을 보존하면서도, RN 앱에서 필요한 UX 상태를 안전하게 표현하게 해 준다.
