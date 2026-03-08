import { Module } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import { EventEmitterModule } from "@nestjs/event-emitter";
import { BooksModule } from "./books/books.module";
import { EventsModule } from "./events/events.module";
import { Book } from "./books/entities/book.entity";

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: "better-sqlite3",
      database: process.env.DB_PATH || ":memory:",
      entities: [Book],
      synchronize: true,
    }),
    EventEmitterModule.forRoot(),
    BooksModule,
    EventsModule,
  ],
})
export class AppModule {}
