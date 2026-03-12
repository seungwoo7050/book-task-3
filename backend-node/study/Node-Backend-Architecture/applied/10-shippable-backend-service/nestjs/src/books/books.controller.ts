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
  UseGuards,
  ValidationPipe,
} from "@nestjs/common";
import { ApiBearerAuth, ApiBody, ApiOperation, ApiTags } from "@nestjs/swagger";
import { BooksService } from "./books.service";
import { CreateBookDto } from "./dto/create-book.dto";
import { UpdateBookDto } from "./dto/update-book.dto";
import { JwtAuthGuard } from "../auth/guards/jwt-auth.guard";
import { RolesGuard } from "../auth/guards/roles.guard";
import { Roles } from "../auth/decorators/roles.decorator";
import { Role } from "../auth/entities/user.entity";

@ApiTags("books")
@Controller("books")
export class BooksController {
  constructor(
    @Inject(BooksService)
    private readonly booksService: BooksService,
  ) {}

  @ApiOperation({ summary: "List public books" })
  @Get()
  findAll() {
    return this.booksService.findAll();
  }

  @ApiOperation({ summary: "Get a public book by id" })
  @Get(":id")
  findOne(@Param("id") id: string) {
    return this.booksService.findOne(id);
  }

  @ApiBearerAuth()
  @ApiOperation({ summary: "관리자 권한으로 책을 생성한다" })
  @ApiBody({ type: CreateBookDto })
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(Role.ADMIN)
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

  @ApiBearerAuth()
  @ApiOperation({ summary: "관리자 권한으로 책을 수정한다" })
  @ApiBody({ type: UpdateBookDto })
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(Role.ADMIN)
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

  @ApiBearerAuth()
  @ApiOperation({ summary: "관리자 권한으로 책을 삭제한다" })
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles(Role.ADMIN)
  @Delete(":id")
  @HttpCode(HttpStatus.NO_CONTENT)
  remove(@Param("id") id: string) {
    return this.booksService.remove(id);
  }
}
