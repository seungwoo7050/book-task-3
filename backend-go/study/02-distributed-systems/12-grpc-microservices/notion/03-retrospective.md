# 회고 — gRPC로 마이크로서비스를 만들어본 뒤

## 무엇을 만들었나

Product Catalog gRPC 서비스. Proto 정의(6 RPC), 서버(인메모리 store + interceptor), 클라이언트(retry + load balancing). 의존성: `google.golang.org/grpc`, `google.golang.org/protobuf`.

## 잘된 점

**Contract-first 설계**가 강제된다. `.proto` 파일이 클라이언트와 서버를 동시에 정의한다. REST에서 Swagger/OpenAPI를 "선택적으로" 작성하는 것과 달리, gRPC에서는 proto가 없으면 코드 자체를 생성할 수 없다.

**Interceptor 패턴**이 HTTP 미들웨어(06, 07)와 동일한 구조다. logging → auth → handler 체인이 프로토콜이 바뀌어도 유지된다. HTTP에서 경험한 미들웨어 사고방식이 gRPC에서도 그대로 적용됐다.

**Store의 재사용성**. ProductStore는 gRPC를 전혀 모른다. 05-08에서 Repository를 HTTP와 분리한 것처럼, 여기서도 store는 순수 Go 구조체다. gRPC 서비스 레이어가 store를 호출하고 proto 메시지로 변환한다.

## 아쉬운 점

**proto 코드 생성을 건너뛰었다.** `protoc`이 생성하는 인터페이스와 메시지 타입 없이, hand-written shim으로 작업했다. 실무에서는 코드 생성 파이프라인(protoc + go plugin)을 반드시 구축해야 한다.

**Stream interceptor에 인증이 없다.** ListProducts와 PriceWatch가 인증 없이 접근 가능하다. 실무에서는 stream interceptor에도 auth를 넣어야 한다.

**TLS가 없다.** `insecure.NewCredentials()`를 사용했다. 프로덕션에서는 TLS 인증서를 설정해야 한다. HTTP에서 HTTPS가 필수인 것처럼, gRPC에서도 TLS가 기본이다.

## 커리큘럼에서의 위치

| 계층 | 프로젝트 | 통신 |
|------|---------|------|
| HTTP/JSON | 05-09 | REST |
| **gRPC/Protobuf** | **12** | **RPC** |
| 분산 로그 | 13 | Raft + gRPC |

12는 "서비스 간 통신"의 기초를 놓는다. 13에서는 gRPC 위에 분산 합의(Raft)를 구현한다.

## 다음 프로젝트로의 전달

13(distributed-log-core)에서 gRPC를 사용해 로그 복제 API를 노출한다. 12에서 배운 proto 정의, interceptor, streaming 패턴이 직접 재활용된다.
