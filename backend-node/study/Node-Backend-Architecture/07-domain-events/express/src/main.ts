import { createApp } from "./app";
import { createDatabase } from "./database/init";

const PORT = Number(process.env.PORT) || 3000;
const db = createDatabase(process.env.DB_PATH || "bookstore.db");
const app = createApp(db);

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

process.on("SIGINT", () => { db.close(); process.exit(0); });
