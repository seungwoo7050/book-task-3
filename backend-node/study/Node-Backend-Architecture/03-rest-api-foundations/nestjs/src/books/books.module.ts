import { Module } from "@nestjs/common";
import { BooksController } from "./books.controller";
import { BooksService } from "./books.service";

/**
 * BooksModule — Feature module for the Books domain.
 *
 * Registers BooksController and BooksService.
 * The DI container automatically injects BooksService into BooksController.
 */
@Module({
  controllers: [BooksController],
  providers: [BooksService],
})
export class BooksModule {}
