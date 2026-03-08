# Integration Architecture

## Module Composition

```text
AppModule
├── RuntimeModule
│   ├── RuntimeConfigService
│   └── RedisService
├── TypeOrmModule.forRootAsync()
├── EventEmitterModule.forRoot()
├── AuthModule
├── BooksModule
├── EventsModule
└── HealthController
```

## 핵심 변화

- DB를 SQLite에서 Postgres로 교체했다.
- `synchronize: true` 대신 migration을 사용한다.
- Redis를 event bus 대신 cache와 throttling 상태 저장에만 쓴다.
- Swagger와 health endpoint를 추가해 reviewer가 브라우저와 curl만으로 구조를 확인할 수 있게 했다.

## 데이터 흐름

1. request id가 부여된다.
2. DTO validation이 먼저 실행된다.
3. 보호 라우트는 JWT와 role guard를 통과해야 한다.
4. service가 Postgres와 Redis를 조합해 읽기 또는 쓰기를 수행한다.
5. 쓰기 성공 시 이벤트가 발행되고 캐시가 무효화된다.
