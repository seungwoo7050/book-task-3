import Database from "better-sqlite3";

export function initDatabase(db: Database.Database): void {
  db.exec(`
    CREATE TABLE IF NOT EXISTS books (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      author TEXT NOT NULL,
      published_year INTEGER NOT NULL,
      genre TEXT NOT NULL,
      price REAL NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    )
  `);
}

export function createDatabase(filename: string = ":memory:"): Database.Database {
  const db = new Database(filename);
  db.pragma("journal_mode = WAL");
  initDatabase(db);
  return db;
}
