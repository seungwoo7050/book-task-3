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
 * BooksController — Handles HTTP requests for the /books resource.
 *
 * Compare with the Express version:
 *   - No manual `bind(this)` — NestJS preserves context automatically.
 *   - No `asyncHandler` — NestJS catches async errors internally.
 *   - No `res.status().json()` — just return the value.
 *   - No separate router file — decorators define routes inline.
 */
@Controller("books")
export class BooksController {
  constructor(
    @Inject(BooksService)
    private readonly booksService: BooksService,
  ) {}

  /** GET /books */
  @Get()
  findAll(): Book[] {
    return this.booksService.findAll();
  }

  /** GET /books/:id */
  @Get(":id")
  findOne(@Param("id") id: string): Book {
    return this.booksService.findOne(id);
  }

  /** POST /books */
  @Post()
  create(@Body() dto: CreateBookDto): Book {
    return this.booksService.create(dto);
  }

  /** PUT /books/:id */
  @Put(":id")
  update(@Param("id") id: string, @Body() dto: UpdateBookDto): Book {
    return this.booksService.update(id, dto);
  }

  /** DELETE /books/:id */
  @Delete(":id")
  @HttpCode(204)
  remove(@Param("id") id: string): void {
    this.booksService.remove(id);
  }
}
