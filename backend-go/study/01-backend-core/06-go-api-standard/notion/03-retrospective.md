# 회고 — 이 과제에서 얻은 것

## 코드 구조 분리의 가치

파일 하나에 모든 것을 넣어도 "돌아가기는" 한다. 하지만 routes.go, handlers.go, errors.go, middleware.go로 분리하면 "어디를 봐야 하는지"가 즉시 드러난다. 이 분리 패턴은 이후 모든 API 과제에서 반복된다.

## 미들웨어는 프레임워크 없이도 만들 수 있다

`func(next http.Handler) http.Handler` 시그니처 하나만 알면 미들웨어를 쌓을 수 있다. chi나 echo가 해 주는 미들웨어 체인을 직접 만들어 보니, "프레임워크가 추상화하고 있는 것"이 무엇인지 명확해졌다.

## graceful shutdown은 한 번 구현하면 계속 쓴다

이 과제에서 만든 `serve` 함수의 shutdown 패턴은 거의 모든 Go 서버에 그대로 복사해서 쓸 수 있다. 한 번 이해하고 나면 뒤 과제에서 반복적으로 사용된다.

## log/slog는 구조화된 로깅의 표준이다

Go 1.21에서 추가된 `log/slog`를 처음 써 봤다. 키-값 쌍으로 구조화된 로그를 남기면 나중에 grep이나 로그 분석 도구로 필터링하기 쉬워진다. 이전까지 `log.Printf`를 쓰던 것과 비교하면 큰 개선이다.

## 다음 과제와의 연결

이 과제의 `application` struct, middleware 체인, JSON envelope 패턴은 07번(auth), 08번(SQL store), 09번(관찰가능성)에서 거의 그대로 재사용된다.
