# 같은 API를 Express와 NestJS로 만들면 보이는 것들

## 왜 같은 걸 두 번 만드는가

이 과제는 Books CRUD API를 Express와 NestJS로 각각 만든다. 같은 기능을 두 프레임워크로 나란히 구현하면, "프레임워크가 대신해 주는 것"과 "직접 해야 하는 것"의 경계가 선명해진다.

이전 과제(`02-http-and-api-basics`)에서 프레임워크 없이 HTTP를 다뤘기 때문에, 이제 Express가 무엇을 추상화하는지 바로 체감할 수 있다. 그리고 Express에서 직접 했던 일들을 NestJS가 어떻게 선언적으로 바꾸는지를 비교하면, 각 프레임워크의 설계 철학이 드러난다.

## Express 레인: 직접 조립하는 감각

### 계층 분리를 수동으로 만든다

Express는 프레임워크가 구조를 강제하지 않는다. 파일 하나에 모든 걸 넣어도 동작한다. 하지만 이 과제에서는 의도적으로 계층을 나눴다:

- `services/book.service.ts` — 비즈니스 로직과 데이터 저장소. Express에 대한 의존이 전혀 없다.
- `controllers/book.controller.ts` — HTTP 요청을 받아서 서비스를 호출하고 응답을 보낸다.
- `routes/book.router.ts` — URL 패턴과 컨트롤러 메서드를 매핑한다.
- `app.ts` — 모든 의존성을 조립하는 composition root.

이 분리를 직접 해보면, "왜 서비스에 `req`를 넘기면 안 되는가"가 체감된다. 서비스가 HTTP 객체를 몰라야 단위 테스트에서 HTTP 없이 비즈니스 로직만 검증할 수 있다.

### 수동 DI와 this 바인딩

Express에서는 DI 컨테이너가 없다. `app.ts`에서 직접 `new BookService()` → `new BookController(bookService)` → `createBookRouter(controller)`로 의존성을 조립한다.

그리고 Express의 라우터 콜백으로 클래스 메서드를 등록할 때, `this` 컨텍스트가 유실되는 문제가 있다. 그래서 생성자에서 `this.findAll = this.findAll.bind(this)`를 명시적으로 해줘야 한다. 이건 작지만 실수하기 쉬운 부분이고, NestJS에서는 아예 발생하지 않는 문제다.

### asyncHandler를 직접 만든다

Express는 async 핸들러의 에러를 자동으로 잡지 않는다. `async` 함수에서 에러가 나면 unhandled rejection이 된다. 그래서 `asyncHandler`라는 유틸리티를 직접 만들어서 `try/catch` 없이 async 핸들러를 안전하게 등록할 수 있게 했다.

이건 Express 5에서 자동 지원될 예정이지만, Express 4에서는 여전히 직접 해야 한다.

## NestJS 레인: 선언적으로 정의하는 감각

### 데코레이터가 구조를 강제한다

NestJS에서는 같은 기능이 완전히 다른 모습으로 구현된다:

- `@Controller("books")` — 이 클래스가 `/books` 경로를 담당한다
- `@Get()`, `@Post()`, `@Put(":id")`, `@Delete(":id")` — 라우트 정의
- `@Param("id")`, `@Body()` — 파라미터 추출
- 반환값을 그대로 돌려주면 NestJS가 JSON 직렬화와 상태 코드를 알아서 처리한다

Express에서 `res.status(201).json(book)`으로 직접 했던 일을, NestJS에서는 `return this.booksService.create(dto)`로 끝낸다.

### DI 컨테이너가 자동으로 연결한다

`@Injectable()` 데코레이터를 서비스에 붙이면, NestJS DI 컨테이너가 컨트롤러의 생성자에 자동으로 주입한다. Express에서 직접 `new` 했던 조립 과정이 사라진다.

`BooksModule`은 서비스와 컨트롤러를 묶는 역할을 하고, `AppModule`이 `BooksModule`을 import하면 전체 앱이 구성된다. Express에서 `app.ts`가 하던 composition root 역할을 모듈 시스템이 대신한다.

### NotFoundException으로 에러를 처리한다

Express에서는 `findById`가 `undefined`를 반환하면 컨트롤러가 `if (!book)` 검사 후 `res.status(404).json()`을 직접 호출했다. NestJS에서는 서비스가 `throw new NotFoundException()`을 하면 프레임워크가 404 응답을 자동으로 만든다.

이건 에러 처리의 책임이 컨트롤러에서 서비스로 이동한 것이다. 컨트롤러가 더 얇아지는 대신, 서비스가 HTTP 예외를 알게 되는 트레이드오프가 있다.

## 두 레인을 비교하면 보이는 것

| 관점 | Express | NestJS |
|------|---------|--------|
| 라우트 정의 | Router + 콜백 등록 | 데코레이터 |
| DI | 수동 (composition root) | 자동 (DI 컨테이너) |
| this 바인딩 | `bind(this)` 필요 | 불필요 |
| async 에러 처리 | `asyncHandler` 래퍼 필요 | 자동 |
| 응답 전송 | `res.json()` 직접 호출 | return 값으로 자동 |
| 404 처리 | 컨트롤러에서 분기 | `NotFoundException` throw |
| 구조 강제 | 없음 (컨벤션 의존) | 데코레이터 + 모듈 (강제) |

Express는 "자유도가 높은 대신 직접 챙겨야 할 게 많다." NestJS는 "규약을 따르면 대부분 자동으로 된다." 이 트랙에서 Express를 원리 학습 레인으로, NestJS를 실무 적용 레인으로 잡은 이유가 여기에 있다.

## 테스트 전략

두 레인 모두 단위 테스트와 E2E 테스트를 나눠 두었다:

- **단위 테스트**: 서비스의 CRUD 로직만 검증. HTTP 계층 없이 순수 함수/메서드 호출.
- **E2E 테스트**: `supertest`(Express) 또는 `@nestjs/testing`의 `Test.createTestingModule`(NestJS)로 전체 스택을 관통하는 HTTP 요청을 보내서 응답을 검증.

NestJS에서는 E2E 테스트 설정이 별도의 `vitest.e2e.config.ts`로 분리되어 있다.

## 이 과제의 위치와 다음 단계

이 과제를 마치면 두 프레임워크로 동일한 CRUD API를 만들어 본 상태가 된다. 다음 과제인 `04-request-pipeline`에서는 validation, error handling, logging, response shaping을 파이프라인으로 묶어서, 여기서 하드코딩했던 에러 처리와 응답 형식을 공통 규약으로 추출한다.

그리고 여기서 사용한 in-memory 저장소는 `06-persistence-and-repositories`에서 SQLite로 교체되며, `05-auth-and-authorization`에서는 이 CRUD 위에 인증/인가 레이어가 올라간다.
