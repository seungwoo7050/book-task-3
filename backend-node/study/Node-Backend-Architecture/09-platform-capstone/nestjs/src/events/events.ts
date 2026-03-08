export class BookCreatedEvent {
  constructor(
    public readonly bookId: string,
    public readonly title: string,
    public readonly author: string,
    public readonly timestamp: Date = new Date(),
  ) {}
}

export class BookUpdatedEvent {
  constructor(
    public readonly bookId: string,
    public readonly changes: string[],
    public readonly timestamp: Date = new Date(),
  ) {}
}

export class BookDeletedEvent {
  constructor(
    public readonly bookId: string,
    public readonly timestamp: Date = new Date(),
  ) {}
}

export class UserRegisteredEvent {
  constructor(
    public readonly userId: string,
    public readonly username: string,
    public readonly role: string,
    public readonly timestamp: Date = new Date(),
  ) {}
}
