# Debug Log — Realtime Chat

## WatermelonDB 데코레이터 경고

프로젝트 초기에 WatermelonDB를 설치하고 스키마를 정의한 뒤, 실제 Model 클래스를 작성하려 했을 때 데코레이터 관련 TypeScript 경고가 나왔다. `experimentalDecorators`를 켜야 하는 상황이었는데, 이 프로젝트에서는 WatermelonDB의 모델 데코레이터를 직접 사용하지 않고 순수 함수(`createPendingMessage`, `reconcileAck` 등)로 로직을 분리하는 방향을 택했다. 결과적으로 데코레이터 의존성 없이도 핵심 동작을 테스트할 수 있었다.

## FlashList estimatedItemSize 경고

`RealtimeChatStudyApp.tsx`에서 FlashList를 처음 렌더링했을 때 `estimatedItemSize` 관련 경고가 콘솔에 찍혔다. FlashList v2에서는 `estimatedItemSize`를 명시하지 않으면 내부적으로 측정을 시도하지만 경고를 띄운다. 메시지 행 높이가 일정하지 않았기 때문에 고정값을 주기보다는 `getItemType`만 지정하고 경고는 수용하기로 했다.

## Jest에서 WatermelonDB import 에러

테스트 파일에서 `storageSchema.ts`를 import하면 WatermelonDB의 네이티브 모듈 바인딩이 없어서 에러가 발생했다. 이를 해결하기 위해 테스트 대상을 `chatModel.ts`(순수 함수)로 한정하고, 스키마 파일은 앱 코드에서만 import하도록 분리했다. 이 경험은 "네이티브 의존성이 있는 코드와 순수 로직을 물리적으로 분리해야 테스트가 편하다"는 교훈을 남겼다.

## reconcileAck에서 status 타입 불일치

초기 구현에서 `reconcileAck` 함수가 status를 문자열 `'sent'`로 할당할 때 TypeScript가 `string` 타입으로 추론해서 `'pending' | 'sent'` 유니언과 맞지 않는 문제가 있었다. `as const` assertion이나 명시적 타입 캐스팅으로 해결했다. 작은 문제지만, 유니언 타입 기반 상태 모델링에서 반복적으로 마주치는 패턴이라 기록해 둔다.
