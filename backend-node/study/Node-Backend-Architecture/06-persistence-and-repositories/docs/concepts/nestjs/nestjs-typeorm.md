# NestJS + TypeORM Integration

## Setup

### 1. Root Module Configuration

```typescript
@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: "better-sqlite3",
      database: ":memory:",
      entities: [Book],
      synchronize: true,
    }),
    BooksModule,
  ],
})
export class AppModule {}
```

### 2. Feature Module Registration

```typescript
@Module({
  imports: [TypeOrmModule.forFeature([Book])],
  controllers: [BooksController],
  providers: [BooksService],
})
export class BooksModule {}
```

`TypeOrmModule.forFeature([Book])` registers the `Book` repository in this module's scope.

### 3. Inject Repository in Service

```typescript
@Injectable()
export class BooksService {
  constructor(
    @InjectRepository(Book)
    private readonly bookRepository: Repository<Book>,
  ) {}

  findAll(): Promise<Book[]> {
    return this.bookRepository.find();
  }

  async findOne(id: string): Promise<Book> {
    const book = await this.bookRepository.findOneBy({ id });
    if (!book) throw new NotFoundException(`Book ${id} not found`);
    return book;
  }
}
```

## Testing

For testing, use `TypeOrmModule.forRoot()` with `:memory:` database in the test module:

```typescript
const module = await Test.createTestingModule({
  imports: [
    TypeOrmModule.forRoot({
      type: "better-sqlite3",
      database: ":memory:",
      entities: [Book],
      synchronize: true,
    }),
    BooksModule,
  ],
}).compile();
```

Each test module gets its own in-memory database, providing full isolation.

## 근거 요약

- 근거: [문서] `backend-architecture/04-database/README.md`
- 근거: [문서] `backend-architecture/04-database/lab-report.md`
- 근거: [문서] `backend-architecture/04-database/nestjs-impl/docs/README.md`
- 근거: [문서] `backend-architecture/04-database/nestjs-impl/devlog/README.md`
