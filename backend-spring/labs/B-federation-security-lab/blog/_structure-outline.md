# B-federation-security-lab structure outline

## 글 목표

- 이 랩을 "강화 기능을 구현한 랩"보다 "강화 기능의 계약을 먼저 잘라 낸 scaffold"로 보이게 쓴다.
- federation, 2FA, audit가 모두 아직 공개 demo surface 수준이라는 점을 숨기지 않는다.

## 글 순서

1. live provider 대신 callback contract를 먼저 고정한 단계
2. TOTP와 audit를 같은 상태 변화로 묶은 단계
3. SecurityConfig와 validation 부재가 드러내는 현재 취약한 표면
4. 컨테이너 기반 Gradle 검증과 수동 bootRun 응답으로 마무리

## 반드시 넣을 코드 앵커

- `FederationSecurityApiTest.googleCallbackAndAuditFlowWork()`
- `FederationSecurityDemoService.authorize()`
- `FederationSecurityDemoService.setupTotp()`
- `FederationSecurityDemoService.verifyTotp()`
- `SecurityConfig.securityFilterChain()`

## 반드시 넣을 CLI

```bash
docker run --rm -u $(id -u):$(id -g) -v "$PWD":/workspace -w /workspace \
  eclipse-temurin:21-jdk bash -lc './gradlew spotlessCheck checkstyleMain checkstyleTest'
docker run --rm -u $(id -u):$(id -g) -v "$PWD":/workspace -w /workspace \
  eclipse-temurin:21-jdk bash -lc './gradlew test'
docker run --rm -u $(id -u):$(id -g) -p 18081:8080 -v "$PWD":/workspace -w /workspace \
  eclipse-temurin:21-jdk bash -lc './gradlew bootRun'
```

## 핵심 개념

- federation의 핵심은 provider SDK보다 callback contract다.
- 2FA는 현재 보안 enforcement보다 상태 변화 설명용 surface에 가깝다.
- audit가 존재한다는 사실과 audit가 보호된다는 사실은 다르다.
