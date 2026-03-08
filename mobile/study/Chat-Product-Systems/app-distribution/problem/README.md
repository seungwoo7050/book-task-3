# Problem: App Distribution

> Status: VERIFIED
> Scope: modern RN release rehearsal
> Last Checked: 2026-03-08

## Objective

Take the verified `realtime-chat` snapshot and prepare it for release work without turning this
repository into a credential dump. The goal is to prove that the app can be packaged,
environment-separated, and validated by automation before a real store upload workflow is wired.

## Why This Project Exists

- `realtime-chat` proves product behavior.
- `app-distribution` proves release discipline.
- The project stays separate so the learning path keeps product work and release work distinct.

## Required Scope

1. Copy the verified `realtime-chat` app as the release candidate.
2. Add environment separation for `development`, `staging`, `production`.
3. Add Fastlane lanes for validation, Android signing rehearsal, and iOS archive dry-run.
4. Add a GitHub Actions workflow that runs typecheck, tests, and rehearsal validation.
5. Add a local rehearsal command that creates reproducible summary artifacts.

## Explicit Non-Goals

- Real App Store / Play Store upload
- Real signing secrets in the repository
- App Center / CodePush integration
- OTA update infrastructure

## Deliverables

- `react-native/fastlane/Fastfile`
- `react-native/.github/workflows/mobile-release.yml`
- `react-native/.env.*.example`
- `react-native/scripts/release-rehearsal.mjs`
- `react-native/release/rehearsal-summary.json`

## Canonical Commands

```bash
make test
make app-build
make app-test
make release-rehearsal
```

## Evaluation

- `make test`: scaffold validation
- `make app-build`: React Native TypeScript typecheck
- `make app-test`: Jest suite
- `make release-rehearsal`: validate env separation, fastlane/workflow presence, emit rehearsal summary

The project is complete only when all four commands are reproducible without requiring private
credentials.
          case codePush.SyncStatus.DOWNLOADING_PACKAGE:
            console.log('Downloading update...');
            break;
          case codePush.SyncStatus.INSTALLING_UPDATE:
            console.log('Installing update...');
            break;
          case codePush.SyncStatus.UP_TO_DATE:
            console.log('App is up to date');
            break;
          case codePush.SyncStatus.UPDATE_INSTALLED:
            console.log('Update installed');
            break;
        }
      }
    );
  }, []);

  return <NavigationContainer>...</NavigationContainer>;
}

export default codePush(codePushOptions)(App);
```

### CLI Commands

```bash
# Release to staging
appcenter codepush release-react -a YourOrg/ChatApp-iOS -d Staging
appcenter codepush release-react -a YourOrg/ChatApp-Android -d Staging

# Promote staging to production
appcenter codepush promote -a YourOrg/ChatApp-iOS -s Staging -d Production
appcenter codepush promote -a YourOrg/ChatApp-Android -s Staging -d Production

# Rollback
appcenter codepush rollback -a YourOrg/ChatApp-iOS -d Production
appcenter codepush rollback -a YourOrg/ChatApp-Android -d Production

# Target specific binary version
appcenter codepush release-react -a YourOrg/ChatApp-iOS -d Production -t "1.2.x"
```

---

## Part 4: Environment Configuration

### Requirements

Implement environment-based configuration:

1. **.env files** — Separate `.env.staging` and `.env.production`
2. **Build schemes** — iOS schemes for staging/production
3. **Build flavors** — Android Gradle flavors for staging/production
4. **Runtime config** — Access environment variables in TypeScript

### Environment Files

```bash
# .env.staging
API_URL=https://staging-api.example.com
WS_URL=wss://staging-api.example.com/ws
CODEPUSH_KEY_IOS=your-staging-ios-key
CODEPUSH_KEY_ANDROID=your-staging-android-key
ENVIRONMENT=staging

# .env.production
API_URL=https://api.example.com
WS_URL=wss://api.example.com/ws
CODEPUSH_KEY_IOS=your-production-ios-key
CODEPUSH_KEY_ANDROID=your-production-android-key
ENVIRONMENT=production
```

### Config Module

```typescript
import Config from 'react-native-config';

export const config = {
  apiUrl: Config.API_URL!,
  wsUrl: Config.WS_URL!,
  codepushKey: Platform.select({
    ios: Config.CODEPUSH_KEY_IOS,
    android: Config.CODEPUSH_KEY_ANDROID,
  }),
  environment: Config.ENVIRONMENT as 'staging' | 'production',
  isProduction: Config.ENVIRONMENT === 'production',
};
```

---

## Part 5: CI/CD with GitHub Actions

### Requirements

Create a GitHub Actions workflow that:

1. **On PR** — Run lint, type check, and tests
2. **On merge to develop** — Build staging, deploy to TestFlight/Internal Testing, push CodePush staging
3. **On merge to main** — Build production, deploy to App Store/Play Store, promote CodePush to production

### Workflow Skeleton

```yaml
name: CI/CD

on:
  pull_request:
    branches: [develop, main]
  push:
    branches: [develop, main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npx tsc --noEmit
      - run: npm test

  build-ios:
    needs: lint-and-test
    if: github.event_name == 'push'
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          bundler-cache: true
      - run: npm ci
      - run: cd ios && pod install
      - run: bundle exec fastlane ios deploy_testflight
        if: github.ref == 'refs/heads/develop'
      - run: bundle exec fastlane ios deploy_appstore
        if: github.ref == 'refs/heads/main'

  build-android:
    needs: lint-and-test
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      - run: npm ci
      - run: bundle exec fastlane android deploy_internal
        if: github.ref == 'refs/heads/develop'
      - run: bundle exec fastlane android deploy_production
        if: github.ref == 'refs/heads/main'
```

---

## Part 6: Version Management

### Requirements

1. **Semantic versioning** — Follow semver (major.minor.patch)
2. **Automated bump** — Use `fastlane-plugin-versioning` or a custom script
3. **Changelog** — Generate from conventional commits
4. **Git tagging** — Tag releases with version

### Fastlane Version Bump

```ruby
desc "Bump version"
lane :bump do |options|
  type = options[:type] || "patch"  # major, minor, patch

  # iOS
  increment_version_number(
    xcodeproj: "ios/ChatApp.xcodeproj",
    bump_type: type
  )
  increment_build_number(xcodeproj: "ios/ChatApp.xcodeproj")

  # Android
  android_set_version_name(
    gradle_file: "android/app/build.gradle",
    version_name: get_version_number(xcodeproj: "ios/ChatApp.xcodeproj")
  )
  android_set_version_code(
    gradle_file: "android/app/build.gradle"
  )

  # Commit and tag
  version = get_version_number(xcodeproj: "ios/ChatApp.xcodeproj")
  git_commit(path: ["ios/", "android/"], message: "chore: bump version to #{version}")
  add_git_tag(tag: "v#{version}")
end
```

---

## Test Criteria

1. **Fastlane iOS**: Build lane completes without errors, IPA is generated
2. **Fastlane Android**: Build lane completes, APK/AAB is generated
3. **CodePush**: JS bundle deploys to staging, can be promoted to production
4. **Environments**: Staging/production configs are correctly applied at build time
5. **CI/CD**: GitHub Actions workflow runs lint, test, and build stages
6. **Versioning**: Version bumps update both iOS and Android version numbers

## Evaluation

```bash
make build-check
```
