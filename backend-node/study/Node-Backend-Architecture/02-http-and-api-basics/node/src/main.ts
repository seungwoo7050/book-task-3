import { createApp } from "./app";

const port = Number(process.env.PORT ?? "3000");
const server = createApp();

server.listen(port, () => {
  process.stdout.write(`HTTP basics server listening on ${port}\n`);
});
