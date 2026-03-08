import { Module } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import { EventEmitterModule } from "@nestjs/event-emitter";
import { AuthModule } from "./auth/auth.module";
import { BooksModule } from "./books/books.module";
import { EventsModule } from "./events/events.module";
import { Book } from "./books/entities/book.entity";
import { User } from "./auth/entities/user.entity";

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: "better-sqlite3",
      database: process.env.DB_PATH || ":memory:",
      entities: [Book, User],
      synchronize: true,
    }),
    EventEmitterModule.forRoot(),
    AuthModule,
    BooksModule,
    EventsModule,
  ],
})
export class AppModule {}
