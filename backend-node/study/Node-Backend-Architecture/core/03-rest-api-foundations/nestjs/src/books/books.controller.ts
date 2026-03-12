import {
  Controller,
  Inject,
  Get,
  Post,
  Put,
  Delete,
  Param,
  Body,
  HttpCode,
} from "@nestjs/common";
import { BooksService } from "./books.service";
import { CreateBookDto } from "./dto/create-book.dto";
import { UpdateBookDto } from "./dto/update-book.dto";
import { Book } from "./entities/book.entity";

/**
 * BooksController - /books resource의 HTTP 요청을 처리한다.
 *
 * Express 버전과 비교하면:
 *   - 수동 `bind(this)`가 필요 없다. NestJS가 context를 자동으로 보존한다.
 *   - `asyncHandler`가 필요 없다. NestJS가 async 오류를 내부에서 처리한다.
 *   - `res.status().json()` 대신 값을 반환하면 된다.
 *   - 별도 router 파일 없이 decorator로 route를 인라인 정의한다.
 */
@Controller("books")
export class BooksController {
  constructor(
    @Inject(BooksService)
    private readonly booksService: BooksService,
  ) {}

  /** GET /books 목록 조회 */
  @Get()
  findAll(): Book[] {
    return this.booksService.findAll();
  }

  /** GET /books/:id 단건 조회 */
  @Get(":id")
  findOne(@Param("id") id: string): Book {
    return this.booksService.findOne(id);
  }

  /** POST /books 생성 */
  @Post()
  create(@Body() dto: CreateBookDto): Book {
    return this.booksService.create(dto);
  }

  /** PUT /books/:id 수정 */
  @Put(":id")
  update(@Param("id") id: string, @Body() dto: UpdateBookDto): Book {
    return this.booksService.update(id, dto);
  }

  /** DELETE /books/:id 삭제 */
  @Delete(":id")
  @HttpCode(204)
  remove(@Param("id") id: string): void {
    this.booksService.remove(id);
  }
}
