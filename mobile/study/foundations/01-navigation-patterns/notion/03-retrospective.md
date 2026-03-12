# 03 — Retrospective: 네비게이션 아키텍처 회고

## 무엇을 만들었나

React Navigation v7 기반으로 4층 중첩 navigator 구조를 구현했다.
RootStack → Drawer → Tabs → HomeStack/ProfileStack.
10개 화면, 5개 deep link 경로, 커스텀 header, 커스텀 drawer content, 인증 상태 기반 conditional rendering까지 포함한 완성된 네비게이션 체계다.

## 잘된 점

### 1. 타입 먼저, 화면 나중

`types.ts`에서 ParamList 타입을 모두 정의한 뒤 화면을 구현하는 순서가 효과적이었다.
`NavigatorScreenParams<>`로 하위 navigator의 params를 상위로 합성하는 방식은 처음에는 복잡해 보이지만,
한 번 잡아 놓으면 잘못된 navigate() 호출을 컴파일 타임에 잡아준다.

실제로 `NotificationsScreen`에서 `navigate('Main', { screen: 'HomeTab', params: { screen: 'Home' } })`를 호출할 때
params 구조를 잘못 넣으면 바로 타입 에러가 뜬다. 런타임에 "화면이 안 열린다"는 식의 디버깅이 필요 없다.

### 2. Deep Link state hydration 패턴

URL에 id만 넣고 title은 state hydration에서 보완하는 패턴은 깔끔했다.
`visitRoutes()` 유틸로 중첩 state를 재귀 순회하는 구조도 재사용 가능하다.
실무에서는 이 패턴에 API 호출을 넣어 서버 데이터로 state를 풍부하게 만들 수 있다.

### 3. Drawer의 session 상태 관리

Drawer 레벨에서 session state를 관리하고 하위 navigator로 prop drilling하는 구조가 명확했다.
`useMemo`로 drawer content를 메모이제이션한 것도 불필요한 리렌더를 방지하는 좋은 습관이었다.

## 아쉬운 점

### 1. getParent() 체인의 취약성

HomeScreen에서 Drawer를 열기 위해 `getParent()?.getParent()`를 사용한 것은 구조에 강하게 결합된다.
navigator 사이에 레이어가 하나 추가되면 이 코드가 깨진다.
React Navigation의 navigator `id` prop을 활용하면 `getParent('DrawerId')`로 안전하게 접근할 수 있는데,
이 프로젝트에서는 적용하지 않았다.

### 2. 테스트 부재

이 프로젝트에는 자동화된 테스트가 없다.
linking의 URL → state 매핑, `resolveNavigationState()`의 title 보완 로직,
conditional drawer items의 표시/숨김 등은 단위 테스트로 검증할 수 있었다.
특히 `resolveNavigationState()`는 순수 함수이므로 테스트하기 가장 쉬운 후보였다.

### 3. 화면 컴포넌트의 비즈니스 로직 부재

모든 화면이 navigate()와 UI 렌더링만 하고 실제 데이터 fetching이나 상태 관리는 없다.
네비게이션 학습에 집중한 의도적인 결정이지만,
실무에서는 `useFocusEffect`로 데이터를 새로고침하거나 `beforeRemove` listener로 저장 확인을 하는 패턴이 중요하다.

## 설계 판단 기록

### 왜 RootStack을 Drawer 위에 두었나?

NotFound 화면을 modal로 표시하기 위해서다.
NotFound가 Drawer 내부에 있으면 drawer 메뉴가 함께 보이는데, 이는 "이 URL은 유효하지 않다"는 메시지와 맞지 않다.
Drawer 바깥의 RootStack에 두면 전체 화면 위에 modal로 뜨므로 의도가 명확해진다.

### 왜 SearchTab에 Stack을 쓰지 않았나?

SearchTab은 단일 화면이다. Stack으로 감쌀 필요가 없는 화면을 굳이 Stack에 넣으면
불필요한 navigator 레이어가 추가되고 header 관리도 복잡해진다.
탭에 직접 화면을 넣으면 `headerShown: false`로 탭 레벨 header를 숨기고
화면 자체의 ScreenShell이 전체 UI를 담당한다.

### 왜 ProfileHub에 initialParams를 넣었나?

`ProfileHub`에 `initialParams={{ userId: 'designer-07' }}`을 설정한 이유는
deep link 없이 탭을 통해 ProfileTab으로 진입했을 때도 `route.params.userId`가 존재하도록 보장하기 위해서다.
`userId`가 required param인데 initialParams가 없으면 undefined로 접근해 런타임 에러가 날 수 있다.

### 왜 theme을 별도 파일로 분리했나?

`palette`와 `navigationTheme`을 `theme.ts`로 분리한 것은 색상 토큰을 한 곳에서 관리하기 위해서다.
AppHeader, AppScreens, RootNavigator 세 파일이 모두 palette를 import하므로,
색상을 바꿀 때 한 파일만 수정하면 된다.

## 다음 단계에서 시도할 것

1. **navigator id 부여**: `getParent('drawerId')` 패턴으로 구조 변경에 안전한 코드 만들기
2. **`resolveNavigationState` 단위 테스트**: 다양한 URL 입력에 대한 state 검증
3. **`useFocusEffect` 활용**: 탭 전환 시 데이터 새로고침이나 analytics 이벤트 전송
4. **Screen listeners**: `beforeRemove`로 편집 중 이탈 시 저장 확인 대화상자 구현
