import { Module } from "@nestjs/common";
import { AppEventListener } from "./app-event.listener";

@Module({
  providers: [AppEventListener],
})
export class EventsModule {}
