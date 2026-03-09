# IAM 정책 평가를 코드로 체감하기

## 왜 이 과제를 만들었나

AWS IAM 정책 문법은 공식 문서를 읽으면 금방 파악할 수 있다.
`Effect`, `Action`, `Resource`라는 세 키워드만 알면 정책 JSON을 눈으로 읽는 건 어렵지 않다.

그런데 "이 요청이 왜 허용되었는지", "왜 거부되었는지"를 **설명**하라고 하면 이야기가 달라진다.
문법을 아는 것과 평가 흐름을 설명하는 것 사이에는 꽤 큰 간극이 있었다.

이 과제는 그 간극을 코드로 메우는 출발점이다.
"IAM policy를 읽고 요청에 대한 허용/거부 결정을 내리는 엔진"을 직접 만들면서,
정책이 어떻게 statement 단위로 매칭되고 최종 결정이 나오는지를 체감하는 것이 목표였다.

## 핵심 규칙 세 가지

코드를 작성하기 전에 먼저 정리한 규칙은 세 가지뿐이었다.

1. **Explicit Deny가 모든 Allow보다 우선한다.** Deny statement가 하나라도 매칭되면 결과는 무조건 거부다.
2. **Action과 Resource가 둘 다 맞아야 statement가 적용된다.** Action만 맞고 Resource가 다르면 해당 statement는 건너뛴다.
3. **어떤 Allow statement도 매칭되지 않으면 기본 거부(implicit deny)다.** IAM의 기본 태도는 "허용하지 않은 것은 금지"다.

이 세 가지만 코드로 옮기면, 이후 IAM analyzer나 control plane에서 정책을 다룰 때 자연스럽게 이어진다.

## 설계 선택

### 엔진을 순수 함수로 만든 이유

`evaluate_policy` 함수는 외부 상태 없이 policy dict와 request dict를 받아서 Decision을 반환한다.
AWS SDK를 호출하지도, DB를 읽지도 않는다.

이렇게 한 이유는 두 가지다.
- **테스트가 즉시 가능하다.** fixture JSON만 있으면 어디서든 테스트를 돌릴 수 있다.
- **이후 과제에서 조합하기 쉽다.** 과제 04(IAM Policy Analyzer)와 과제 10(Control Plane)에서
  이 엔진의 판단 흐름을 그대로 확장한다.

### wildcard 매칭에 fnmatch를 쓴 이유

AWS IAM의 wildcard 매칭은 `*`와 `?`를 지원한다.
Python 표준 라이브러리의 `fnmatch.fnmatchcase`가 정확히 같은 문법이라서,
정규표현식을 직접 만드는 것보다 의도가 명확하고 실수가 적었다.

### Statement 결과를 전부 남긴 이유

매칭 여부와 관계없이 모든 statement의 결과를 `StatementResult` 리스트로 반환한다.
최종 허용/거부만 알면 되는 게 아니라, "어떤 statement가 적용되었고 어떤 것은 왜 무시되었는지"를
설명할 수 있어야 했기 때문이다.

이 결정이 이후 CLI에서 `explain` 명령을 만들 때 바로 써먹을 수 있는 구조가 되었다.

## 실제로 만들어 본 뒤에 체감한 것

처음에는 "Allow가 있으면 허용, 없으면 거부"라고 단순하게 생각했다.
그런데 테스트를 작성하면서 Deny statement가 Allow보다 뒤에 있어도 전체 결과를 거부로 뒤집는 케이스를 만들었고,
그제서야 "explicit deny는 순서가 아니라 우선순위"라는 걸 코드로 느꼈다.

또 하나, Action만 맞고 Resource가 안 맞는 경우를 처음에는 "partial match"로 취급하려 했는데,
IAM에서는 partial match라는 개념 자체가 없다. 맞거나 안 맞거나 둘 중 하나다.
이 이진 판단이 나중에 CSPM rule engine에서 finding을 만들 때도 같은 패턴으로 반복된다.

## 이 과제의 위치

이 프로젝트는 전체 트랙의 가장 첫 번째 과제다.
여기서 만든 `evaluate_policy`의 판단 흐름이 뒤 과제에서 이렇게 이어진다:

- **과제 04 (IAM Policy Analyzer)**: 허용/거부 판단이 아니라, "이 정책이 왜 위험한지"를
  finding으로 바꾸는 분석기를 만든다.
- **과제 10 (Control Plane)**: IAM policy scan을 API 요청으로 받아서 DB에 finding을 저장하고,
  예외 처리와 리포트까지 연결한다.

정책 문법을 외우는 것보다, 요청이 어떻게 statement에 걸리고 왜 최종 결정이 나오는지를
코드로 설명할 수 있어야 이후 과제들이 자연스럽다.

## 한계와 v1 범위

이 과제는 의도적으로 범위를 좁혔다.
- Condition keys, Principal evaluation, Policy variables는 다루지 않는다.
- SCP(Service Control Policy)와 Permission Boundary도 범위 밖이다.
- 실제 AWS API를 호출하지 않는다.

이 모든 것은 "평가 흐름의 뼈대"를 먼저 체감하기 위한 선택이었다.
뼈대가 잡힌 뒤에 Condition이나 SCP를 얹는 것은 확장이지, 처음부터 전부 넣는 것은 학습이 아니라 구현 연습이다.
