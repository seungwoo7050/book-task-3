# Problem: Navigation Patterns

> Status: VERIFIED
> Scope: nested navigator + deep linking
> Last Checked: 2026-03-12

## 문제 요약

Stack, Tab, Drawer를 중첩한 React Native 앱을 만들고, external URL이 특정 화면으로 바로 진입하도록
Deep Linking까지 연결하는 과제다.

## 왜 이 문제가 커리큘럼에 필요한가

기초 단계에서 화면 구조를 잘못 잡으면 이후 모든 제품형 과제에서 state와 route가 엉킨다.
이 프로젝트는 "화면 이동을 기능 추가가 아니라 구조 설계 문제로 볼 수 있는가"를 묻는다.

## 제공 자료

- 기존 navigation 과제 요구사항
- `problem/code/README.md`의 참고 코드 스캐폴드
- `problem/data/README.md`의 fixture 안내

## 필수 요구사항

1. typed params를 사용하는 Stack navigator
2. badge와 custom style을 갖춘 Bottom Tab navigator
3. conditional action이 있는 custom Drawer navigator
4. `myapp://` scheme과 path-based Deep Linking
5. unknown path를 처리하는 fallback route
6. iOS/Android 공통으로 설명 가능한 route 구조

## 의도적 비범위

- 실제 인증 서버 연동
- universal link 배포 설정
- analytics/observability 추가

## 평가/검증 기준

```bash
make test
```

- push/pop과 params 전달이 정상 동작해야 한다.
- tab 전환, badge, drawer action이 렌더링돼야 한다.
- deep link가 올바른 nested state로 매핑돼야 한다.
- `npm --prefix ../react-native run verify`가 통과해야 한다.

## 원문/출처 보존 위치

- [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
