/**
 * Application entry point.
 *
 * TODO:
 *   1. Create instances: BookService → BookController → BookRouter.
 *   2. Wire dependencies via constructors (manual DI).
 *   3. Mount the router on "/books".
 *   4. Add JSON body parsing middleware.
 *   5. Start the server on PORT 3000.
 */

import express from "express";

const app = express();
const PORT = process.env.PORT || 3000;

// TODO: Wire dependencies and mount routes

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

export default app;
