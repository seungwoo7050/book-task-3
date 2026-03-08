import { Module } from "@nestjs/common";
import { BookEventListener } from "./book-event.listener";

@Module({
  providers: [BookEventListener],
  exports: [BookEventListener],
})
export class EventsModule {}
