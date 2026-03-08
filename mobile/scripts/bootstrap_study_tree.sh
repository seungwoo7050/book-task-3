#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

write_file() {
  local path="$1"
  shift
  mkdir -p "$(dirname "$path")"
  cat >"$path"
}

copy_problem_dir() {
  local source_dir="$1"
  local target_dir="$2"

  mkdir -p "$target_dir"
  rm -rf "$target_dir/problem"
  cp -R "$source_dir/problem" "$target_dir/"
  find "$target_dir/problem" -name '.gitkeep' -delete
  mkdir -p "$target_dir/problem/code" "$target_dir/problem/data" "$target_dir/problem/script"

  if [[ ! -f "$target_dir/problem/code/README.md" ]]; then
    write_file "$target_dir/problem/code/README.md" <<EOF
# Starter Code

이 디렉터리는 원본 문제에서 제공된 starter code 위치다.
현재 legacy 기준선에는 추적할 starter code가 없어 빈 상태로 유지한다.
EOF
  fi

  if [[ ! -f "$target_dir/problem/data/README.md" ]]; then
    write_file "$target_dir/problem/data/README.md" <<EOF
# Problem Data

이 디렉터리는 문제에서 제공된 fixture나 sample data 위치다.
현재 legacy 기준선에는 추적할 데이터 파일이 없다.
EOF
  fi

  write_file "$target_dir/problem/SOURCE-PROVENANCE.md" <<EOF
# Source Provenance

- Legacy source: \`${source_dir#"$ROOT_DIR"/}/problem\`
- Copied into: \`${target_dir#"$ROOT_DIR"/}/problem\`
- Migration rule: 원본 문제 설명과 스캐폴드만 유지하고, 사용자 구현은 \`react-native/\` 또는 \`node-server/\`에 둔다.
EOF
}

create_common_project_files() {
  local project_dir="$1"
  local title="$2"
  local status="$3"
  local summary="$4"
  local source_path="$5"
  local verify_cmd="$6"
  local rn_status="$7"
  local concepts_text="$8"
  local references_text="$9"

  mkdir -p \
    "$project_dir/docs/concepts" \
    "$project_dir/docs/references" \
    "$project_dir/notion"

  write_file "$project_dir/README.md" <<EOF
# ${title}

Status: ${status}

## Summary

${summary}

## Source Provenance

- Legacy source: \`${source_path}\`
- Study path: \`${project_dir#"$ROOT_DIR"/}\`

## Build/Test

\`\`\`bash
${verify_cmd}
\`\`\`

## Current Status

- problem scaffold: copied from legacy or rewritten for study use
- react-native implementation: ${rn_status}
- docs migration: in-progress
EOF

  write_file "$project_dir/docs/README.md" <<EOF
# Docs: ${title}

Status: ${status}

이 디렉터리는 장기적으로 남길 개념 문서와 참고 자료를 모은다.

## Sections

- [concepts/README.md](concepts/README.md)
- [references/README.md](references/README.md)
EOF

  write_file "$project_dir/docs/concepts/README.md" <<EOF
# Concepts

${concepts_text}
EOF

  write_file "$project_dir/docs/references/README.md" <<EOF
# References

${references_text}
EOF

  write_file "$project_dir/notion/00-problem-framing.md" <<EOF
# Problem Framing

- Project: ${title}
- Legacy source: \`${source_path}\`
- Current migration status: ${status}
- Questions to resolve:
  - What counts as a minimal working implementation?
  - Which requirements are only documented and not yet runnable?
EOF

  write_file "$project_dir/notion/01-approach-log.md" <<EOF
# Approach Log

초기 마이그레이션 스캐폴드만 생성했다.
후속 구현 시 선택지, 의존성, 설계 결정을 기록한다.
EOF

  write_file "$project_dir/notion/02-debug-log.md" <<EOF
# Debug Log

아직 디버깅 기록은 없다.
검증 명령 실패와 복구 과정을 이 파일에 축적한다.
EOF

  write_file "$project_dir/notion/03-retrospective.md" <<EOF
# Retrospective

현재는 구조 재정비 단계다.
구현과 검증이 끝나면 학습 결과와 약점을 정리한다.
EOF

  write_file "$project_dir/notion/04-knowledge-index.md" <<EOF
# Knowledge Index

- Legacy path: \`${source_path}\`
- Public docs path: \`${project_dir#"$ROOT_DIR"/}/docs\`
- Next step: reusable knowledge만 public docs로 승격하고, 과정 중심 기록은 notion에 남긴다.
EOF
}

create_react_native_placeholder() {
  local project_dir="$1"
  local title="$2"
  local status="$3"
  local build_cmd="$4"
  local test_cmd="$5"
  local gaps="$6"
  local note="$7"

  mkdir -p \
    "$project_dir/react-native/src" \
    "$project_dir/react-native/tests" \
    "$project_dir/react-native/ios" \
    "$project_dir/react-native/android"

  write_file "$project_dir/react-native/README.md" <<EOF
# React Native Implementation

Status: ${status}

## Problem Scope Covered

${title}의 React Native 구현 디렉터리다.

## Build Command

\`\`\`bash
${build_cmd}
\`\`\`

## Test Command

\`\`\`bash
${test_cmd}
\`\`\`

## Known Gaps

${gaps}

## Implementation Notes

${note}
EOF

  write_file "$project_dir/react-native/src/README.md" <<EOF
# Source Layout

앱 소스는 이 디렉터리에 둔다.
현재는 프로젝트 골격만 생성되었고, 파일럿을 제외한 나머지 과제는 후속 구현 대상이다.
EOF

  write_file "$project_dir/react-native/tests/README.md" <<EOF
# Tests

Jest 또는 통합 테스트를 이 디렉터리에 둔다.
현재는 프로젝트별 구현 완료 후 검증 케이스를 추가할 예정이다.
EOF

  write_file "$project_dir/react-native/ios/README.md" <<EOF
# iOS Workspace

React Native CLI 앱의 iOS 프로젝트 파일 위치다.
파일럿 이외 프로젝트는 실제 native scaffold를 아직 생성하지 않았다.
EOF

  write_file "$project_dir/react-native/android/README.md" <<EOF
# Android Workspace

React Native CLI 앱의 Android 프로젝트 파일 위치다.
파일럿 이외 프로젝트는 실제 native scaffold를 아직 생성하지 않았다.
EOF
}

create_offline_sync_problem() {
  local project_dir="$1"

  mkdir -p "$project_dir/problem/code" "$project_dir/problem/data" "$project_dir/problem/script"

  write_file "$project_dir/problem/README.md" <<'EOF'
# Problem: Offline Sync Foundations

Status: planned

## Objective

Build a focused React Native study project that teaches offline write queues,
retry policies, sync replay, and conflict resolution before the full realtime chat case study.

## Scope

1. Local mutation queue with idempotency keys
2. Connectivity-aware flush scheduling
3. Retry with capped backoff and DLQ isolation
4. Pull-after-push sync cycle
5. Deterministic tests for queue state transitions

## Deliverables

- A small React Native client that manages offline tasks
- A fake API layer or local test server for deterministic sync scenarios
- Jest coverage for queue transitions and replay behavior
EOF

  write_file "$project_dir/problem/code/README.md" <<'EOF'
# Starter Code

이 프로젝트는 레거시에 없던 새 브리지 과제다.
starter code는 제공하지 않고, 문제 정의와 테스트 가능한 구현을 새로 설계한다.
EOF

  write_file "$project_dir/problem/data/README.md" <<'EOF'
# Problem Data

필수 fixture는 아직 없다.
후속 구현 시 sync queue 시나리오용 JSON fixture를 추가한다.
EOF

  write_file "$project_dir/problem/script/README.md" <<'EOF'
# Scripts

문제 스캐폴드 검증 스크립트는 후속 단계에서 추가한다.
현재는 프로젝트 정의와 구현 골격만 생성했다.
EOF

  write_file "$project_dir/problem/SOURCE-PROVENANCE.md" <<'EOF'
# Source Provenance

- Origin: study-only bridge project
- Reason added: realtime-chat 진입 전에 오프라인 큐와 동기화 개념을 분리 학습하기 위해 추가했다.
- Legacy gap: 기존 레거시 트리는 WatermelonDB/WebSocket 통합 문제로 바로 진입해 학습 간격이 컸다.
EOF
}

create_capstone_assets() {
  local project_dir="$1"

  mkdir -p "$project_dir/problem/code/contracts"
  cp "$ROOT_DIR/legacy/04-capstone/mobile-product-capstone/solve/solution/shared/contracts.ts" \
    "$project_dir/problem/code/contracts/contracts.ts"
  write_file "$project_dir/problem/code/contracts/README.md" <<'EOF'
# Shared Contracts

캡스톤의 공통 DTO와 도메인 계약을 문제 경계로 승격한 위치다.
클라이언트와 서버 구현은 이 계약을 기준으로 맞춘다.
EOF

  rm -rf "$project_dir/node-server"
  cp -R "$ROOT_DIR/legacy/04-capstone/mobile-product-capstone/solve/solution/server" \
    "$project_dir/node-server"
  while IFS= read -r -d '' file; do
    perl -0pi -e 's#../../shared/contracts#../../problem/code/contracts/contracts#g' "$file"
  done < <(find "$project_dir/node-server/src" -type f -name '*.ts' -print0)

  write_file "$project_dir/node-server/README.md" <<'EOF'
# Node Server Implementation

Status: in-progress

## Problem Scope Covered

캡스톤의 로컬 API, realtime, audit backend 구현을 보관한다.

## Build Command

```bash
cd study/Incident-Ops-Capstone/incident-ops-mobile/node-server
npm install
npm test
```

## Test Command

```bash
cd study/Incident-Ops-Capstone/incident-ops-mobile/node-server
npm test
```

## Known Gaps

- 모바일 클라이언트와 end-to-end로 통합된 재현 절차는 아직 새 study 구조에 맞게 다시 정리해야 한다.

## Implementation Notes

- 이 구현은 legacy 캡스톤 서버를 기준으로 복사했다.
- 공통 계약은 problem/code/contracts로 분리했다.
EOF
}

mkdir -p "$ROOT_DIR/docs" "$ROOT_DIR/study"

copy_problem_dir \
  "$ROOT_DIR/legacy/01-foundation/navigation" \
  "$ROOT_DIR/study/Mobile-Foundations/navigation"
copy_problem_dir \
  "$ROOT_DIR/legacy/01-foundation/virtualized-list" \
  "$ROOT_DIR/study/Mobile-Foundations/virtualized-list"
copy_problem_dir \
  "$ROOT_DIR/legacy/01-foundation/gestures" \
  "$ROOT_DIR/study/Mobile-Foundations/gestures"
copy_problem_dir \
  "$ROOT_DIR/legacy/02-architecture/bridge-vs-jsi" \
  "$ROOT_DIR/study/React-Native-Architecture/bridge-vs-jsi"
copy_problem_dir \
  "$ROOT_DIR/legacy/02-architecture/native-modules" \
  "$ROOT_DIR/study/React-Native-Architecture/native-modules"
copy_problem_dir \
  "$ROOT_DIR/legacy/03-chat-product/realtime-chat" \
  "$ROOT_DIR/study/Chat-Product-Systems/realtime-chat"
copy_problem_dir \
  "$ROOT_DIR/legacy/03-chat-product/app-distribution" \
  "$ROOT_DIR/study/Chat-Product-Systems/app-distribution"
copy_problem_dir \
  "$ROOT_DIR/legacy/04-capstone/mobile-product-capstone" \
  "$ROOT_DIR/study/Incident-Ops-Capstone/incident-ops-mobile"
copy_problem_dir \
  "$ROOT_DIR/legacy/04-capstone/mobile-product-capstone" \
  "$ROOT_DIR/study/Incident-Ops-Capstone/incident-ops-mobile-client"

create_common_project_files \
  "$ROOT_DIR/study/Mobile-Foundations/navigation" \
  "Navigation Patterns" \
  "in-progress" \
  "Stack, Tab, Drawer, Deep Linking을 실제 React Native 앱으로 구현하는 파일럿 프로젝트다." \
  "legacy/01-foundation/navigation" \
  "cd study/Mobile-Foundations/navigation/react-native && npm run verify" \
  "actual app implementation included" \
  "Navigation lifecycle, nested navigator state, typed params를 다룬다." \
  "Legacy docs와 official React Navigation 자료를 정리한다."

create_common_project_files \
  "$ROOT_DIR/study/Mobile-Foundations/virtualized-list" \
  "Virtualized List Performance" \
  "planned" \
  "대형 리스트 렌더링, virtualization 전략, 메모리/프레임 분석을 다룬다." \
  "legacy/01-foundation/virtualized-list" \
  "cd study/Mobile-Foundations/virtualized-list/react-native && echo 'implementation pending'" \
  "planned" \
  "FlatList, FlashList, windowing, measurement를 정리한다." \
  "Legacy docs의 flashlist, memory-profiling 자료를 승격할 예정이다."

create_common_project_files \
  "$ROOT_DIR/study/Mobile-Foundations/gestures" \
  "Gestures And Reanimated" \
  "planned" \
  "Gesture Handler와 Reanimated 기반 인터랙션을 연습한다." \
  "legacy/01-foundation/gestures" \
  "cd study/Mobile-Foundations/gestures/react-native && echo 'implementation pending'" \
  "planned" \
  "gesture state machine, shared values, animation debugging을 정리한다." \
  "Legacy docs의 reanimated, performance-debugging 자료를 참조한다."

create_common_project_files \
  "$ROOT_DIR/study/React-Native-Architecture/bridge-vs-jsi" \
  "Bridge Vs JSI" \
  "planned" \
  "React Native Bridge와 JSI/TurboModules/Fabric 비용 구조를 비교한다." \
  "legacy/02-architecture/bridge-vs-jsi" \
  "cd study/React-Native-Architecture/bridge-vs-jsi/react-native && echo 'implementation pending'" \
  "planned" \
  "bridge serialization, host objects, Fabric rendering cost를 정리한다." \
  "Legacy docs의 jsi, fabric, turbomodules 자료를 참조한다."

create_common_project_files \
  "$ROOT_DIR/study/React-Native-Architecture/native-modules" \
  "Native Modules" \
  "planned" \
  "Swift/Kotlin 기반 커스텀 네이티브 모듈 설계를 다룬다." \
  "legacy/02-architecture/native-modules" \
  "cd study/React-Native-Architecture/native-modules/react-native && echo 'implementation pending'" \
  "planned" \
  "platform module API 설계, cross-platform boundary, new architecture readiness를 정리한다." \
  "Legacy docs의 swift-modules, kotlin-modules 자료를 참조한다."

create_common_project_files \
  "$ROOT_DIR/study/Chat-Product-Systems/offline-sync-foundations" \
  "Offline Sync Foundations" \
  "planned" \
  "오프라인 큐와 재시도 정책을 채팅 앱 전에 분리 학습하는 브리지 프로젝트다." \
  "study-designed project" \
  "cd study/Chat-Product-Systems/offline-sync-foundations/react-native && echo 'implementation pending'" \
  "planned" \
  "queue state machine, idempotency, replay order를 정리한다." \
  "새 프로젝트이므로 구현 과정에서 references를 추가한다."

create_common_project_files \
  "$ROOT_DIR/study/Chat-Product-Systems/realtime-chat" \
  "Realtime Chat" \
  "planned" \
  "WebSocket, 로컬 저장소, offline-first sync를 통합하는 제품형 과제다." \
  "legacy/03-chat-product/realtime-chat" \
  "cd study/Chat-Product-Systems/realtime-chat/react-native && echo 'implementation pending'" \
  "planned" \
  "message sync, optimistic update, presence, conflict resolution을 정리한다." \
  "Legacy docs의 websocket, offline-first, sync-conflict-resolution 자료를 참조한다."

create_common_project_files \
  "$ROOT_DIR/study/Chat-Product-Systems/app-distribution" \
  "App Distribution" \
  "planned" \
  "Fastlane, CodePush, CI/CD 기반 배포 자동화 과제다." \
  "legacy/03-chat-product/app-distribution" \
  "cd study/Chat-Product-Systems/app-distribution/react-native && echo 'implementation pending'" \
  "planned" \
  "build lanes, signing, OTA rollout policy를 정리한다." \
  "Legacy docs의 fastlane, codepush, secrets-management 자료를 참조한다."

create_common_project_files \
  "$ROOT_DIR/study/Incident-Ops-Capstone/incident-ops-mobile" \
  "Incident Ops Mobile" \
  "in-progress" \
  "승인, 감사 로그, 오프라인 복구를 포함한 모바일 제품 캡스톤이다." \
  "legacy/04-capstone/mobile-product-capstone" \
  "cd study/Incident-Ops-Capstone/incident-ops-mobile/node-server && npm test" \
  "planned" \
  "approval flow, auditability, replayable demo를 정리한다." \
  "Legacy capstone docs와 demo artifacts를 참조하되, 재현 가능한 근거만 승격한다."

create_common_project_files \
  "$ROOT_DIR/study/Incident-Ops-Capstone/incident-ops-mobile-client" \
  "Incident Ops Mobile Client" \
  "in-progress" \
  "기존 capstone 도메인을 유지하면서 RN 채용 제출용 완성작으로 다시 구성한 최종 과제다." \
  "legacy/04-capstone/mobile-product-capstone + study/Incident-Ops-Capstone/incident-ops-mobile" \
  "cd study/Incident-Ops-Capstone/incident-ops-mobile-client/react-native && npm run verify" \
  "runnable app implementation included" \
  "client architecture, outbox replay, testing pyramid를 정리한다." \
  "기존 capstone docs와 새 RN 구현 근거를 함께 참조한다."

create_react_native_placeholder \
  "$ROOT_DIR/study/Mobile-Foundations/virtualized-list" \
  "대형 리스트 성능 분석" \
  "planned" \
  "echo 'implementation pending'" \
  "echo 'implementation pending'" \
  "- 실제 React Native CLI scaffold 미생성\n- 성능 측정 기준 재정의 필요" \
  "FlatList와 FlashList 비교용 독립 앱으로 구현할 예정이다."

create_react_native_placeholder \
  "$ROOT_DIR/study/Mobile-Foundations/gestures" \
  "Gesture/Reanimated 실험" \
  "planned" \
  "echo 'implementation pending'" \
  "echo 'implementation pending'" \
  "- 실제 React Native CLI scaffold 미생성\n- 플랫폼 제스처 충돌 케이스 정리 필요" \
  "swipe, drag, spring animation 예제를 포함할 예정이다."

create_react_native_placeholder \
  "$ROOT_DIR/study/React-Native-Architecture/bridge-vs-jsi" \
  "Bridge와 JSI 비교 앱" \
  "planned" \
  "echo 'implementation pending'" \
  "echo 'implementation pending'" \
  "- 실제 React Native CLI scaffold 미생성\n- 측정용 benchmark 시나리오 재정의 필요" \
  "JS bridge serialization과 JSI direct call을 같은 기준으로 비교할 예정이다."

create_react_native_placeholder \
  "$ROOT_DIR/study/React-Native-Architecture/native-modules" \
  "Native Module 실습 앱" \
  "planned" \
  "echo 'implementation pending'" \
  "echo 'implementation pending'" \
  "- 실제 React Native CLI scaffold 미생성\n- iOS/Android 양쪽 모듈 parity 설계 필요" \
  "sensor, battery, vibration 성격의 모듈 후보를 나중에 정한다."

create_react_native_placeholder \
  "$ROOT_DIR/study/Chat-Product-Systems/offline-sync-foundations" \
  "Offline Sync 브리지 앱" \
  "planned" \
  "echo 'implementation pending'" \
  "echo 'implementation pending'" \
  "- 실제 React Native CLI scaffold 미생성\n- fake API 또는 local server 설계 필요" \
  "queue visualizer와 deterministic tests를 우선 구현할 예정이다."

create_react_native_placeholder \
  "$ROOT_DIR/study/Chat-Product-Systems/realtime-chat" \
  "Realtime Chat 제품 앱" \
  "planned" \
  "echo 'implementation pending'" \
  "echo 'implementation pending'" \
  "- 실제 React Native CLI scaffold 미생성\n- offline-sync-foundations 이후 재구성 예정" \
  "WatermelonDB, WebSocket, optimistic UI를 분리된 단계로 구현할 예정이다."

create_react_native_placeholder \
  "$ROOT_DIR/study/Chat-Product-Systems/app-distribution" \
  "Distribution 학습 앱" \
  "planned" \
  "echo 'implementation pending'" \
  "echo 'implementation pending'" \
  "- 실제 React Native CLI scaffold 미생성\n- 배포 파이프라인용 샘플 앱 범위 재정의 필요" \
  "배포 스크립트와 signing 문서를 함께 정리할 예정이다."

create_react_native_placeholder \
  "$ROOT_DIR/study/Incident-Ops-Capstone/incident-ops-mobile" \
  "Incident Ops Mobile 클라이언트" \
  "planned" \
  "echo 'implementation pending'" \
  "echo 'implementation pending'" \
  "- 실제 React Native CLI scaffold 미생성\n- node-server와의 계약 소비 방식 결정 필요" \
  "클라이언트 구현은 navigation 파일럿 이후 별도로 이관한다."

create_react_native_placeholder \
  "$ROOT_DIR/study/Incident-Ops-Capstone/incident-ops-mobile-client" \
  "Incident Ops Mobile 최종 클라이언트" \
  "in-progress" \
  "cd react-native && npm run typecheck" \
  "cd react-native && npm test" \
  "- 실제 저장소에는 독립 RN 앱이 추적된다.\n- bootstrap 스크립트는 최소 골격만 재생성한다." \
  "최종 저장소 상태에서는 이 placeholder 대신 완성된 RN 앱이 존재한다."

create_offline_sync_problem \
  "$ROOT_DIR/study/Chat-Product-Systems/offline-sync-foundations"

create_capstone_assets \
  "$ROOT_DIR/study/Incident-Ops-Capstone/incident-ops-mobile"

create_capstone_assets \
  "$ROOT_DIR/study/Incident-Ops-Capstone/incident-ops-mobile-client"

echo "study tree bootstrapped under $ROOT_DIR/study"
