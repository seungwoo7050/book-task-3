# Curriculum Map

이 저장소는 React Native 역량을 단계별 질문으로 나눈 학습 레포다. 새 구조는
`foundations -> architecture -> product-systems -> capstone` 순서를 고정해
각 프로젝트의 위치 이유가 README에서 바로 드러나도록 만든다.

## 1. foundations

- `01-navigation-patterns`
- `02-virtualized-list-performance`
- `03-gestures-and-reanimated`

이 단계는 화면 구조, 리스트 성능, 상호작용 품질처럼 RN 기본기를 먼저 고정한다.
목표는 "화면이 돌아간다"가 아니라 상태 구조와 사용자 체감 품질을 설명할 수 있는 것이다.

## 2. architecture

- `01-bridge-vs-jsi`
- `02-native-modules`

이 단계는 RN runtime 경계와 JS/native 계약을 다룬다.
기초 화면 구현 이후에 두는 이유는, 런타임 비용과 네이티브 경계를 추상적으로 배우지 않고
실제 앱 문맥에서 이해하게 하기 위해서다.

## 3. product-systems

- `01-offline-sync-foundations`
- `02-realtime-chat`
- `03-app-distribution`

이 단계는 local-first 제품 모델과 release discipline을 분리해서 다룬다.
특히 `01-offline-sync-foundations`를 먼저 두어 queue/retry/idempotency를 독립 변수로 익힌 뒤
`02-realtime-chat`과 `03-app-distribution`으로 올라가게 만든다.

## 4. capstone

- `01-incident-ops-mobile`
- `02-incident-ops-mobile-client`

이 단계는 같은 incident domain을 두 번 다룬다.
첫 프로젝트는 contract와 backend boundary를 증명하는 harness이고,
두 번째 프로젝트는 hiring-facing 제품 완성작이다.

## 설계 원칙

- 루트와 stage README에서 문제 질문과 답안을 먼저 본다.
- 세부 요구사항은 `problem/README.md`에 둔다.
- 구현 세부는 `react-native/README.md`, `node-server/README.md`에 둔다.
- 장문 회고와 디버깅은 `notion/`으로 분리한다.
