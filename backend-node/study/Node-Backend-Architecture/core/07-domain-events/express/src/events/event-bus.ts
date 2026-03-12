import { EventEmitter } from "node:events";
import { EventMap } from "../types/events";

export class EventBus {
  private emitter = new EventEmitter();

  emit<K extends keyof EventMap>(event: K, data: EventMap[K]): void {
    this.emitter.emit(event, data);
  }

  on<K extends keyof EventMap>(event: K, handler: (data: EventMap[K]) => void): void {
    this.emitter.on(event, handler as (...args: unknown[]) => void);
  }

  off<K extends keyof EventMap>(event: K, handler: (data: EventMap[K]) => void): void {
    this.emitter.off(event, handler as (...args: unknown[]) => void);
  }

  removeAllListeners(): void {
    this.emitter.removeAllListeners();
  }
}
