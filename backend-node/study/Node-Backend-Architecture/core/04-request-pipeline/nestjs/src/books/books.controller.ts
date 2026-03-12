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
  HttpStatus,
  ValidationPipe,
} from "@nestjs/common";
import { BooksService } from "./books.service";
import { CreateBookDto } from "./dto/create-book.dto";
import { UpdateBookDto } from "./dto/update-book.dto";

@Controller("books")
export class BooksController {
  constructor(
    @Inject(BooksService)
    private readonly booksService: BooksService,
  ) {}

  @Get()
  findAll() {
    return this.booksService.findAll();
  }

  @Get(":id")
  findOne(@Param("id") id: string) {
    return this.booksService.findOne(id);
  }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  create(
    @Body(
      new ValidationPipe({
        transform: true,
        whitelist: true,
        forbidNonWhitelisted: true,
        expectedType: CreateBookDto,
      }),
    )
    dto: CreateBookDto,
  ) {
    return this.booksService.create(dto);
  }

  @Put(":id")
  update(
    @Param("id") id: string,
    @Body(
      new ValidationPipe({
        transform: true,
        whitelist: true,
        forbidNonWhitelisted: true,
        expectedType: UpdateBookDto,
      }),
    )
    dto: UpdateBookDto,
  ) {
    return this.booksService.update(id, dto);
  }

  @Delete(":id")
  @HttpCode(HttpStatus.NO_CONTENT)
  remove(@Param("id") id: string) {
    this.booksService.remove(id);
  }
}
