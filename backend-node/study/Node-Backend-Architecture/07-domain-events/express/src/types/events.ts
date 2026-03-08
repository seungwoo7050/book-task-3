export interface BookCreatedEvent {
  readonly bookId: string;
  readonly title: string;
  readonly author: string;
  readonly timestamp: Date;
}

export interface BookUpdatedEvent {
  readonly bookId: string;
  readonly changes: string[];
  readonly timestamp: Date;
}

export interface BookDeletedEvent {
  readonly bookId: string;
  readonly timestamp: Date;
}

export interface EventMap {
  "book.created": BookCreatedEvent;
  "book.updated": BookUpdatedEvent;
  "book.deleted": BookDeletedEvent;
}
