# architecture

`architecture`는 React Native runtime과 JS/native 경계를 이해하는 단계다.
기초 UI를 만든 뒤에야 왜 bridge 비용이 문제인지, module contract를 어떻게 고정해야 하는지가 선명해진다.

## 포함 프로젝트

1. [01-bridge-vs-jsi](01-bridge-vs-jsi/README.md)
2. [02-native-modules](02-native-modules/README.md)

## 왜 이 순서인가

- `01-bridge-vs-jsi`는 interop surface의 비용 차이를 계측하게 만든다.
- `02-native-modules`는 typed spec과 codegen으로 boundary를 문서화하게 만든다.

## 다음 단계

runtime과 boundary를 이해한 뒤 [product-systems](../product-systems/README.md)에서
offline-first 제품 모델과 release discipline을 다룬다.
