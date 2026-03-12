# 05 — Development Timeline: 개발 환경·도구 기록

이 문서는 소스 코드만으로는 알 수 없는 CLI 명령, codegen 실행 과정, 환경 설정을 기록한다.

---

## Step 1: 프로젝트 초기화

```bash
cd study/architecture/02-native-modules/react-native
npm install
```

서드파티 의존성 없이 RN 코어만 사용하므로 설치가 빠르다.

## Step 2: Codegen Summary 생성

```bash
# npm 스크립트로 실행
npm run codegen

# 또는 Makefile 타겟
make codegen
```

실행 결과:
```
generated summary written to generated/modules.json
```

파일 확인:
```bash
cat generated/modules.json
```

이 단계는 verify 파이프라인에서 가장 먼저 실행된다.
typecheck와 test보다 앞에 와야 generated 파일이 최신 상태로 존재한다.

## Step 3: 타입 체크 및 테스트

```bash
# 개별 실행
npm run typecheck
npm test

# 전체 검증 (codegen → typecheck → test)
npm run verify
```

테스트는 두 개:
1. MODULE_SPECS가 3개 모듈을 가지는지
2. buildGeneratedSummary()가 정확한 summary를 반환하는지

## Step 4: 시뮬레이터 실행

```bash
# iOS
npm run ios

# Android
npm run android
```

앱은 세 개의 카드를 보여준다.
각 카드에 모듈 이름과 메서드 목록이 표시된다.
interactive 요소가 없으므로 화면 확인이 곧 검증이다.

## Step 5: 실제 React Native Codegen (참고)

이 프로젝트의 codegen은 JS 레벨 summary를 생성하는 것이고,
실제 React Native의 codegen은 native 인터페이스를 생성한다:

```bash
# 실제 RN codegen (full native build 필요)
npx react-native codegen

# iOS에서 codegen 결과 확인
ls ios/build/generated/ios/

# Android에서 codegen 결과 확인
ls android/build/generated/java/
```

실제 codegen을 사용하려면:
1. TurboModule spec을 RN의 codegen 규약에 맞게 작성 (NativeXxx.ts 파일명 규칙)
2. `codegenConfig`를 package.json에 추가
3. `npx react-native codegen` 실행
4. 생성된 native interface를 iOS/Android에서 구현

## Step 6: 검증 파이프라인

```bash
# problem 디렉터리에서 전체 검증
cd ../problem
make test

# 개별 단계
make codegen      # summary 생성
make app-build    # typecheck
make app-test     # jest
```

## TurboModule Spec 작성 규칙 (참고)

실제 TurboModule spec 작성 시 RN codegen이 인식하는 형태:

```typescript
// NativeBatteryModule.ts (파일명 필수: Native + 모듈이름)
import type { TurboModule } from 'react-native';
import { TurboModuleRegistry } from 'react-native';

export interface Spec extends TurboModule {
  getBatteryLevel(): Promise<number>;
  getChargingStatus(): string;
}

export default TurboModuleRegistry.getEnforcing<Spec>('BatteryModule');
```

이 프로젝트의 `specs.ts`는 이 구조의 메타데이터(이름, 메서드 목록)만 정의한 간략 버전이다.

## 사용된 도구 정리

| 도구 | 버전/용도 |
|------|-----------|
| Node.js | >= 22.11.0 |
| npm | 패키지 관리 |
| TypeScript 5.8+ | 타입 체크 (--noEmit) |
| Jest 29.6+ | 테스트 러너 |
| Node.js mjs | codegen-summary.mjs 스크립트 실행 |
| Metro Bundler | JS 번들링 |

## 트러블슈팅 체크리스트

- [ ] `as const` 누락 → MODULE_SPECS의 타입이 string으로 일반화됨을 확인
- [ ] codegen 출력이 예전 값 → `codegen-summary.mjs`의 하드코딩 값 업데이트
- [ ] verify 실패 → 순서 확인: codegen → typecheck → test
- [ ] Metro 캐시 → `npm start -- --reset-cache`
