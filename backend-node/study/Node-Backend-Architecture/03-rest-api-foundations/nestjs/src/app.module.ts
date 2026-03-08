import { Module } from "@nestjs/common";
import { BooksModule } from "./books/books.module";

/**
 * AppModule — Root module of the application.
 *
 * Imports all feature modules. In this assignment, only BooksModule.
 */
@Module({
  imports: [BooksModule],
})
export class AppModule {}
