# Problem

## 목표

HTTP 요청/응답의 기본 모델을 프레임워크 없이 직접 다룬다.

## 과제

1. `GET /health`, `GET /books`, `GET /books/:id`, `POST /books`를 직접 구현한다.
2. JSON 요청 본문을 수동으로 읽고 파싱한다.
3. 잘못된 경로, 잘못된 본문, 없는 리소스에 대해 적절한 status code를 반환한다.
4. 서버 객체를 테스트에서 직접 띄울 수 있게 구성한다.

## 제공 자료

- `problem/code/starter.ts`: 라우트 규약과 타입 골격
- `problem/data/book-payload.json`: 예시 POST 본문
- `problem/script/curl-examples.sh`: 수동 점검 명령

## 최소 성공 기준

- `POST /books` 이후 `GET /books`와 `GET /books/:id`가 동일 데이터를 반환한다.
- 오류 응답이 `400`, `404`, `415`로 분리된다.
- 테스트가 health, create, read, validation 흐름을 모두 덮는다.
