# Navigation Patterns

Status: verified

## Summary

Stack, Tab, Drawer, Deep Linking을 실제 React Native 앱으로 구현하는 파일럿 프로젝트다.

## Source Provenance

- Legacy source: `legacy/01-foundation/navigation`
- Study path: `study/Mobile-Foundations/navigation`

## Build/Test

```bash
cd study/Mobile-Foundations/navigation/problem && make test
cd study/Mobile-Foundations/navigation/react-native && npm run verify
```

## What Works

- Home stack: `Home -> Detail -> Settings -> ProfileDetail`
- bottom tabs with custom tab bar styling and badge
- custom drawer content with conditional sign-in/sign-out actions
- deep-link state mapping for `home`, `detail/:id`, `profile/:userId`, `notifications`, fallback
- Jest and TypeScript verification for the pilot app

## Docs

- [docs/README.md](docs/README.md)
- [docs/concepts/navigation-lifecycle.md](docs/concepts/navigation-lifecycle.md)
- [docs/concepts/deep-link-state-mapping.md](docs/concepts/deep-link-state-mapping.md)
- [docs/concepts/typed-navigation-params.md](docs/concepts/typed-navigation-params.md)

## Current Status

- problem scaffold: copied from legacy or rewritten for study use
- react-native implementation: verified
- docs migration: verified for pilot scope
