# Study Workspace

`study/`는 이 저장소의 실제 학습 트리다.
각 프로젝트는 문제 원문, 실행 가능한 구현, 공개 문서, 로컬 노트를 분리한다.

## Tracks

- [Mobile-Foundations/navigation](Mobile-Foundations/navigation/README.md)
- [Mobile-Foundations/virtualized-list](Mobile-Foundations/virtualized-list/README.md)
- [Mobile-Foundations/gestures](Mobile-Foundations/gestures/README.md)
- [React-Native-Architecture/bridge-vs-jsi](React-Native-Architecture/bridge-vs-jsi/README.md)
- [React-Native-Architecture/native-modules](React-Native-Architecture/native-modules/README.md)
- [Chat-Product-Systems/offline-sync-foundations](Chat-Product-Systems/offline-sync-foundations/README.md)
- [Chat-Product-Systems/realtime-chat](Chat-Product-Systems/realtime-chat/README.md)
- [Chat-Product-Systems/app-distribution](Chat-Product-Systems/app-distribution/README.md)
- [Incident-Ops-Capstone/incident-ops-mobile](Incident-Ops-Capstone/incident-ops-mobile/README.md)
- [Incident-Ops-Capstone/incident-ops-mobile-client](Incident-Ops-Capstone/incident-ops-mobile-client/README.md)

## Progress Snapshot

### Verified Projects

- `Mobile-Foundations/navigation`
- `Mobile-Foundations/virtualized-list`
- `Mobile-Foundations/gestures`
- `React-Native-Architecture/bridge-vs-jsi`
- `React-Native-Architecture/native-modules`
- `Chat-Product-Systems/offline-sync-foundations`
- `Chat-Product-Systems/realtime-chat`
- `Chat-Product-Systems/app-distribution`
- `Incident-Ops-Capstone/incident-ops-mobile`
- `Incident-Ops-Capstone/incident-ops-mobile-client`

현재 `study/`는 시작점, 중간 다리, 시스템 캡스톤, 제품 캡스톤까지 모두 검증된 상태다.
루트 문서는 부족한 슬롯 보고서가 아니라, 검증된 학습 경로와 유지보수 기준을 설명한다.

## Project Shape

각 프로젝트는 기본적으로 다음 구조를 따른다.

- `problem/`: 원문 문제, 제공 자료, 스캐폴드 검증 스크립트
- `react-native/`: 독립 React Native CLI 앱 또는 스택별 구현
- `node-server/`: 캡스톤 전용 백엔드 구현
- `docs/`: 저장소에 남길 짧은 개념 문서와 참고 자료
- `notion/`: 로컬 전용 작업 노트

## Validation

```bash
bash ../scripts/report_study_status.sh
bash ../scripts/verify_study_structure.sh
bash ../scripts/check_study_docs.sh
```
