export class HttpError extends Error {
  public readonly status: number;
  public readonly detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.status = status;
    this.detail = detail;
  }
}

export function assertFound<T>(value: T | null | undefined, detail: string): T {
  if (value === null || value === undefined) {
    throw new HttpError(404, detail);
  }

  return value;
}
